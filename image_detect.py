import os



def check_image(image_path: str) -> dict:


    if (not image_path or not os.path.exists(image_path)):
        return False
    else:

        # isAdultContent = check_Adult_Content(image_path)
        isAdultContent = False
        print("isAdultContent:", isAdultContent)

        return {"isNudeContent": False, "isAdultContent": isAdultContent}
