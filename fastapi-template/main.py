import json
import os
from datetime import datetime  # Import datetime module
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from PIL import Image
from io import BytesIO
from models import MsgPayload, CropRequest
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models_db import ImageLog
from fastapi import Depends

app = FastAPI()
messages_list: dict[int, MsgPayload] = {}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello"}


@app.post("/crop/")
async def crop_image(
    file: UploadFile = File(...),
    crop_data: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # Parse crop_data from JSON string to dictionary
    crop_data_dict = json.loads(crop_data)
    crop_request = CropRequest(**crop_data_dict)

    # Read the uploaded image
    image = Image.open(BytesIO(await file.read()))

    # Perform cropping using the provided coordinates
    cropped_image = image.crop((
        crop_request.x,
        crop_request.y,
        crop_request.x + crop_request.width,
        crop_request.y + crop_request.height
    ))

    # Define the save path
    save_directory = "cropped_images"
    os.makedirs(save_directory, exist_ok=True)  # Create the directory if it doesn't exist

    # Add timestamp to the image name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
    new_image_name = f"cropped_{timestamp}_{file.filename}"
    save_path = os.path.join(save_directory, new_image_name)

    # Save the cropped image to the specified path
    cropped_image.save(save_path)

    # Log the cropped image details in the database
    new_log = ImageLog(
        image_name=new_image_name,
        cropped_image_path=save_path
    )
    db.add(new_log)
    await db.commit()

    # Return the saved path as the response
    return {"message": f"Image saved in this path: {save_path}"}
