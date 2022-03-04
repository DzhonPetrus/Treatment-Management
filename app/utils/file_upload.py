import datetime

async def file_upload(uploaded_file):
    if uploaded_file.filename != '':
        modified_filename = f'{datetime.datetime.now().timestamp()}_{uploaded_file.filename}'
        destination = f"app/static/upload/{modified_filename}"
        with open(destination, 'wb') as image:
            content = await uploaded_file.read()
            image.write(content)
            image.close()
        return modified_filename