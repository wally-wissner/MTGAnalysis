import requests
import zipfile


def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def update():
    download_url("https://mtgjson.com/api/v5/AllPrintings.sqlite.zip", "AllPrintings.sqlite.zip")

    with zipfile.ZipFile("AllPrintings.sqlite.zip", 'r') as zip_ref:
        zip_ref.extract("AllPrintings.sqlite")


if __name__ == "__main__":
    update()
