import tkinter as tk
from tkinter import filedialog as fd
import regex as re
import requests as r
import os

class Archiver:
    def __init__(self, homedir: str=None):
        if homedir is None:
            homedir = fd.askdirectory()
        if not os.path.exists(homedir):
            os.makedirs(homedir)
        
        self.homedir = homedir
        if self.homedir[-1] != '/':
            self.homedir += '/'

        self.root = tk.Tk()
        self._page1()
        self.root.mainloop()

        return
    
    def _go(self, url_box: tk.Text):
        url = url_box.get('1.0', tk.END)
        self.archive(url)

        return
    
    def archive(self, url: str):
        """
        Archive a website to a local directory.
        """
        
        # Check if site has already been downloaded
        if not os.path.exists(self.homedir + url):
            # Make url usable
            url = url.strip()

            # Get html
            request = r.get(url, stream=True)
            
            if request.headers['Content-Type'][:4] != 'text':
                print(request.headers['Content-Type'])
                print(url, 'Non-html')
                return
                
            html = request.text

            # Get usable filename
            filename = re.search(r'(?<=https?://)[^.]+', url).group()
            
            # Write to file
            print('Saving: ', self.homedir + filename + '.html')
            with open(self.homedir + filename + '.html', 'wb') as file:
                file.write(bytes(html, 'utf-8'))
            
            # Download all linked sites
            links = re.findall(r'(?<==")(?:https?:)?//[^ ]*?(?=")', html)
            links += re.findall(r'(?<=src=")[^"]+', html)
            
            # Iterate over links
            for link in links:
                print(link)

                # Fix link if needed
                if link[:4].lower() != 'http':
                    link = re.search(r'https?://[^/\\]+(/|\\)?', url).group() + link
                                
                # Download link
                self.archive(link)
        else:
            print('File exists')
         
        return

    def _page1(self):
        tk.Label(self.root, text='Website archiver (enter URL below)').pack()
        
        url_box = tk.Text(self.root, width=30, height=1)
        url_box.pack()
        tk.Button(self.root, text='Archive', command=lambda:self._go(url_box)).pack()
        
        tk.Button(self.root, text='Quit', command=self.root.destroy).pack()

        return

if __name__ == '__main__':
    a = Archiver()
