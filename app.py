import requests
from tokens import public_key
import json
# Used Mintlify to generate docs in vscode

class PdfApis:
    def __init__(self):
        self.base_url = "https://api.ilovepdf.com/v1"
        self.api_key = self.auth()
        self.headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def auth(self):
        req_url = f"{self.base_url}/auth"
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json"
        }
        payload = json.dumps({"public_key": public_key})
        response = requests.post(req_url, data=payload, headers=headers)
        return json.loads(response.text)['token']
    
    def start_task(self, tool):
        start_url = f'{self.base_url}/start/{tool}'
        response = requests.get(start_url, headers=self.headers)
        return json.loads(response.text)
    
    def upload_file(self, task, server, file_url):
        upload_url = f'https://{server}/v1/upload'
        payload = json.dumps({
            "task": task,
            "cloud_file": file_url
        })
        response = requests.post(upload_url, data=payload, headers=self.headers)
        return json.loads(response.text)['server_filename']
    
    def download_file(self, task, server):
        print("downloading")
        download_url = f'https://{server}/v1/download/{task}'
        response = requests.get(download_url, headers=self.headers)
        return response.content

    def merge_pdfs(self, file_urls, output_filename):
        task_data = self.start_task('merge')
        task, server = task_data['task'], task_data['server']
        
        server_filenames = []
        for file_url in file_urls:
            print("Uploading",file_url)
            server_filenames.append(self.upload_file(task, server, file_url))

        payload = json.dumps({
            "task": task,
            "tool": "merge",
            "files": [
                {"server_filename": filename, "filename": f"server{i}.pdf"} for i, filename in enumerate(server_filenames)]
        })
        print("Processing")
        process_url = f'https://{server}/v1/process'
        response = requests.post(process_url, data=payload, headers=self.headers)

        output_content = self.download_file(task, server)
        with open(f'output/{output_filename}', mode="wb") as file:
            file.write(output_content)
        return 'Done'

    def split_pdfs(self, pdf_url, output_filename):
        task_data = self.start_task('split')
        task, server = task_data['task'], task_data['server']
        
        print("Uploading",pdf_url)
        server_filename = (self.upload_file(task, server, pdf_url))

        payload = json.dumps({
            "task": task,
            "tool": "split",
            "files": [{"server_filename": server_filename, "filename": f"server.pdf"} ]
        })
        print("Processing")
        process_url = f'https://{server}/v1/process'
        response = requests.post(process_url, data=payload, headers=self.headers)

        output_content = self.download_file(task, server)
        with open(f"output/{output_filename}", mode="wb") as file:
            file.write(output_content)
        return "Done"

    def remove_password(self, pdf_url,password,output_filename):
        task_data = self.start_task('unlock')
        task, server = task_data['task'], task_data['server']

        print("Uploading",pdf_url)
        server_filename = self.upload_file(task, server, pdf_url)

        payload = json.dumps({
            "task": task,
            "tool": "unlock",
            "files": [{"server_filename": server_filename, "filename": "server.pdf","password":f"{password}"}]
        })
        print("Processing")
        process_url = f'https://{server}/v1/process'
        response = requests.post(process_url, data=payload, headers=self.headers)

        output_content = self.download_file(task, server)
        with open(f"output/{output_filename}", mode="wb") as file:
            file.write(output_content)
        return "Done"

    def extract_text(self, pdf_url,output_filename):
        task_data = self.start_task('extract')
        task, server = task_data['task'], task_data['server']

        print("Uploading",pdf_url)
        server_filename = self.upload_file(task, server, pdf_url)

        payload = json.dumps({
            "task": task,
            "tool": "extract",
            "files": [{"server_filename": server_filename, "filename": "server.pdf"}]
        })
        print("Processing")
        process_url = f'https://{server}/v1/process'
        response = requests.post(process_url, data=payload, headers=self.headers)

        output_content = self.download_file(task, server)
        with open(f"output/{output_filename}", mode="wb") as file:
            file.write(output_content)
        return "Done"

    def convert_images_to_pdf(self, image_url, output_filename):
        task_data = self.start_task('imagepdf')
        task, server = task_data['task'], task_data['server']

        print("Uploading",image_url)
        server_filename = self.upload_file(task, server, image_url)

        payload = json.dumps({
            "task": task,
            "tool": "imagepdf",
            "files": [{"server_filename": server_filename, "filename": "server.pdf"}]
        })
        print("Processing")
        process_url = f'https://{server}/v1/process'
        response = requests.post(process_url, data=payload, headers=self.headers)

        output_content = self.download_file(task, server)
        with open(f"output/{output_filename}", mode="wb") as file:
            file.write(output_content)
        return "Done"