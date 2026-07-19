from fastapi import APIRouter, File, HTTPException, UploadFile

from .predict import predict_digit

router = APIRouter()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict handwritten digit from uploaded image.
    """

    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="Please upload a valid image file."
            )

        # Read uploaded image
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        # Predict digit
        result = predict_digit(image_bytes)

        return {
            "success": True,
            "message": "Prediction successful.",
            **result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )