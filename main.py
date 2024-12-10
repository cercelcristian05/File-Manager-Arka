import customtkinter as ctk
from tktooltip import ToolTip
import tkinter.messagebox as messagebox
import os, time, subprocess, magic, ffmpeg, sys
from PIL import Image
from cryptography.fernet import Fernet
from tkinterdnd2 import TkinterDnD, DND_FILES
import threading

class Interface:
    def __init__(self):
        self.window = ctk.CTk()

        self.window.title('File Explorer (Advanced)')
        self.window.geometry('800x600')
        self.frame = ctk.CTkFrame(self.window, corner_radius=0, fg_color='#2c3e50')
        self.frame.pack(fill="both", expand=True)
        
        self.history = []
        self.popped_history = []
        self.track = 0
                
        self.initLayout()
        self.window.mainloop()
        
    def handlerConverter(self):
        window = TkinterDnD.Tk()  
        window.title('Converter')
        window.geometry('600x550')
        window.resizable(False, False)

        frame = ctk.CTkFrame(window, corner_radius=0, fg_color='#2c3e50')
        frame.pack(fill="both", expand=True)

        containerDrop = ctk.CTkFrame(frame, corner_radius=5, border_color='#F4EEFF', border_width=2, fg_color='transparent')
        containerDrop.pack(fill="both", padx=10, pady=10)
        
        dropAndGet = ctk.CTkLabel(containerDrop, text='Drag and drop a file here', fg_color='#ecf0f1', text_color='#2c3e50', height=128)
        dropAndGet.pack(fill='x', padx=10, pady=10)

        dropAndGet.drop_target_register(DND_FILES)
        dropAndGet.dnd_bind('<<Drop>>', self.on_drop_n)
        
        containerEntry = ctk.CTkFrame(frame, fg_color='transparent')
        containerEntry.pack()
        
        labelEntry = ctk.CTkLabel(containerEntry, text='Input File', text_color='#F4EEFF')
        labelEntry.pack(side='left', padx=29, pady=5)
        
        self.entryFile = ctk.CTkEntry(containerEntry, corner_radius=3, border_color='#ecf0f1', border_width=1, text_color='#F4EEFF', fg_color='transparent', width=256)
        self.entryFile.pack(side='left', pady=5)
        
        containerOut = ctk.CTkFrame(frame, fg_color='transparent')
        containerOut.pack()
        
        labelOut = ctk.CTkLabel(containerOut, text='Output File', text_color='#F4EEFF')
        labelOut.pack(side='left', padx=25, pady=5)
        
        self.outPath = ctk.CTkEntry(containerOut, corner_radius=3, border_color='#ecf0f1', border_width=1, text_color='#F4EEFF', fg_color='transparent', width=256)
        self.outPath.pack(side='left', pady=5)
        
        containerListOption = ctk.CTkFrame(frame, fg_color='transparent')
        containerListOption.pack()
        
        self.selectedOption = ctk.IntVar(value=-1)
        self.initChoice = []
                
        listOptionOne = ctk.CTkRadioButton(containerListOption, text='IMAGE', text_color='#ecf0f1', value=0, variable=self.selectedOption, fg_color='#ecf0f1', hover_color='#bdc3c7', border_color='#34495e', border_width_checked=5, command=self.updateInit)
        listOptionOne.pack(side='left', pady=10)
        
        listOptionTwo = ctk.CTkRadioButton(containerListOption, text='VIDEO/AUDIO', text_color='#ecf0f1', value=1, variable=self.selectedOption, fg_color='#ecf0f1', hover_color='#bdc3c7', border_color='#34495e', border_width_checked=5, command=self.updateInit)
        listOptionTwo.pack(side='left', pady=10)
        
        containerChoice = ctk.CTkFrame(frame, fg_color='transparent')
        containerChoice.pack()
        
        self.choiceOne = ctk.CTkComboBox(containerChoice, values=self.initChoice, dropdown_fg_color='#ecf0f1', border_color='#ecf0f1', dropdown_hover_color='#bdc3c7', corner_radius=3)
        self.choiceOne.pack(side='left', padx=15, pady=5)
        self.choiceOne.set("")
        
        self.choiceTwo = ctk.CTkComboBox(containerChoice, values=self.initChoice, dropdown_fg_color='#ecf0f1', border_color='#ecf0f1', dropdown_hover_color='#bdc3c7', corner_radius=3)
        self.choiceTwo.pack(side='left', padx=15, pady=5)
        self.choiceTwo.set("")
        
        containerButton = ctk.CTkFrame(frame, fg_color='transparent')
        containerButton.pack(pady=(25,5))
        
        convertButton = ctk.CTkButton(containerButton, text='Convert', text_color='#ecf0f1', fg_color='transparent', hover_color='#34495e', border_color='#ecf0f1', border_width=1, corner_radius=3, command = self.convertOutput)
        convertButton.pack(side='left')
        
        self.displayError = ctk.CTkLabel(frame, text='')
        self.displayError.pack(pady=(10,0))
        
        window.mainloop()
        
    def on_drop_n(self, event):
        file_path = event.data.strip('{}')
        
        self.entryFile.delete(0, 'end')
        self.entryFile.insert(0, file_path)  
        
    def updateInit(self):
        choice = self.selectedOption.get()
        
        if(choice == 0):
            self.initChoice = ['PNG', 'JPEG', 'WEBP']
        elif(choice == 1):
            self.initChoice = ['MP4', 'AVI', 'MKV', 'MOV', 'WEBM', 'MP3', 'OGG', 'WAV', 'OPUS', 'M4A']
            
        self.choiceOne.configure(values=self.initChoice)
        self.choiceTwo.configure(values=self.initChoice)
        
        if self.initChoice:
            self.choiceOne.set(self.initChoice[0])
            self.choiceTwo.set(self.initChoice[0])
        
    def convertOutput(self):
        threading.Thread(target = self.convertOutput, daemon=True).start()
        try:
            getFirstOption = self.choiceOne.get().lower()
            getSecondOption = self.choiceTwo.get().lower()
            getPath = self.entryFile.get()
            getRedirectPath = self.outPath.get()
            
            mime = magic.Magic(mime=True)
            mime_type = mime.from_file(getPath)
            print(mime_type)
            
            if not os.path.isfile(getPath):
                self.displayError.configure(text=f"Expected a file.", text_color='#e74c3c')
                return
                
            if not os.path.isdir(getRedirectPath):
                self.displayError.configure(text=f"Expected a directory.", text_color='#e74c3c')
                return
                
            getVar = os.path.basename(getPath)
            outputFile = os.path.join(getRedirectPath, getVar.replace(getFirstOption, getSecondOption))
            
            if mime_type.startswith("image/"):
                with Image.open(getPath) as img:
                    if img.mode in ("RGBA", "LA"):
                        img = img.convert("RGB")
                    img.save(outputFile, getSecondOption.upper())
            elif mime_type.startswith("audio/") or mime_type.startswith("video/"):
                ffmpeg.input(getPath).output(outputFile).run(overwrite_output=True)
            else:
                self.displayError.configure(text=f"Format unsupported, file is {mime_type}.", text_color='#e74c3c')

            self.displayError.configure(text='Conversion successful.', text_color='#2ecc71')

        except Exception as e:
            self.displayError.configure(text=str(e), text_color='#e74c3c')
        
    def handlerDownloader(self):
        window = ctk.CTk()
        window.title('Downloader')
        window.geometry('400x250')
        window.resizable(False, False)
        
        self.selectedOptionDownload = ctk.IntVar(value=-1)
        self.initChoiceFormat = ['VIDEO', 'AUDIO']
        self.initChoiceResolution = ['720p', '480p', '360p', '144p']
        
        frame = ctk.CTkFrame(window, corner_radius=0, fg_color='#2c3e50')
        frame.pack(fill="both", expand=True)
        
        containerEntry = ctk.CTkFrame(frame, fg_color='transparent')
        containerEntry.pack()
        
        labelEntry = ctk.CTkLabel(containerEntry, text='URL', text_color='#F4EEFF')
        labelEntry.pack(side='left', padx=(0,50), pady=25)
        
        self.entryURL = ctk.CTkEntry(containerEntry, corner_radius=3, border_color='#ecf0f1', border_width=1, text_color='#F4EEFF', fg_color='transparent', width=256)
        self.entryURL.pack(side='left', pady=25)
        
        containerOut = ctk.CTkFrame(frame, fg_color='transparent')
        containerOut.pack()
        
        labelOut = ctk.CTkLabel(containerOut, text='Output File', text_color='#F4EEFF')
        labelOut.pack(side='left', padx=(0,10), pady=3)
        
        self.outDownload = ctk.CTkEntry(containerOut, corner_radius=3, border_color='#ecf0f1', border_width=1, text_color='#F4EEFF', fg_color='transparent', width=256)
        self.outDownload.pack(side='left', pady=3)
        
        containerChoice = ctk.CTkFrame(frame, fg_color='transparent')
        containerChoice.pack()
        
        self.choiceOneDownload = ctk.CTkComboBox(containerChoice, values=self.initChoiceFormat, dropdown_fg_color='#ecf0f1', dropdown_hover_color='#bdc3c7', corner_radius=3)
        self.choiceOneDownload.pack(side='left', padx=15, pady=10)
        self.choiceOneDownload.set("")
        
        self.choiceTwoDownload = ctk.CTkComboBox(containerChoice, values=self.initChoiceResolution, dropdown_fg_color='#ecf0f1', dropdown_hover_color='#bdc3c7', corner_radius=3)
        self.choiceTwoDownload.pack(side='left', padx=15, pady=10)
        self.choiceTwoDownload.set("")
        
        containerButton = ctk.CTkFrame(frame, fg_color='transparent')
        containerButton.pack()
        
        downloadButton = ctk.CTkButton(containerButton, text='Download', text_color='#ecf0f1', fg_color='transparent', hover_color='#34495e', border_color='#ecf0f1', border_width=1, corner_radius=3, command=lambda: self.downloadByUrl(self.entryURL.get()))
        downloadButton.pack(pady=(10,0))
        
        self.displayError = ctk.CTkLabel(frame, text='')
        self.displayError.pack(pady=(10,0))
        
        window.mainloop()
        
    def downloadByUrl(self, url):  
        def _download():
            getPath = self.outDownload.get()
        
            if not os.path.isdir(getPath):
                self.displayError.configure(text=f"Expected a directory.", text_color='#e74c3c')
                return
            
            output_path = os.path.join(getPath, "%(title)s.%(ext)s")

            if self.initChoiceFormat[0] == 'VIDEO':
                self.displayError.configure(text='Downloading video . . .', text_color='#ecf0f1')

                try:
                    resolution = self.choiceTwoDownload.get().replace('p','')
                    print(self.choiceTwoDownload.get())
                    command_video = [
                        "yt-dlp",
                        "-f", f"bv*[height={resolution}]+ba/best",
                        "-o", output_path,
                        url
                    ]
                    subprocess.run(command_video, check=True)
                    self.displayError.configure(text='Download successful. [Video & Audio Mode]', text_color='#2ecc71')

                except Exception as e:
                    print(f"Unexpected error: {e}")
                    self.displayError.configure(text='Something unexpected happened.', text_color='#e74c3c')
                    
            elif self.initChoiceFormat[1] == 'AUDIO':
                self.displayError.configure(text='Downloading audio . . .', text_color='#ecf0f1')

                try:
                    command_audio = [
                        "yt-dlp",
                        "-f", "bestaudio",
                        "-o", output_path,
                        url
                    ]
                    subprocess.run(command_audio, check=True)
                    self.displayError.configure(text='Download successful. [Audio Mode]', text_color='#2ecc71')

                except subprocess.CalledProcessError as e:
                    print(f"Audio-only download failed: {e}")
                    self.displayError.configure(text='Failed to download audio.', text_color='#e74c3c')

                except Exception as e:
                    print(f"Unexpected error: {e}")
                    self.displayError.configure(text='Something unexpected happened.', text_color='#e74c3c')
        threading.Thread(target=_download, daemon=True).start()

    def on_drop(self, event):
        file_path = event.data.strip('{}')
        print(f"File dropped: {file_path}")
        
        self.entryPoint.delete(0, 'end')
        self.entryPoint.insert(0, file_path)     
        
    def handlerEncrypter(self):
        window = TkinterDnD.Tk()  
        window.title('Encrypter')
        window.geometry('600x500')
        window.resizable(False, False)

        frame = ctk.CTkFrame(window, corner_radius=0, fg_color='#2c3e50')
        frame.pack(fill="both", expand=True)

        containerDrop = ctk.CTkFrame(frame, corner_radius=5, border_color='#F4EEFF', border_width=2, fg_color='transparent')
        containerDrop.pack(fill="both", padx=10, pady=10)
        
        dropAndGet = ctk.CTkLabel(containerDrop, text='Drag and drop a file here', fg_color='#ecf0f1', text_color='#2c3e50', height=128)
        dropAndGet.pack(fill='x', padx=10, pady=10)

        dropAndGet.drop_target_register(DND_FILES)
        dropAndGet.dnd_bind('<<Drop>>', self.on_drop)
        
        containerEntry = ctk.CTkFrame(frame, fg_color='transparent')
        containerEntry.pack()
        
        labelEntry = ctk.CTkLabel(containerEntry, text='Input File', text_color='#F4EEFF')
        labelEntry.pack(side='left', padx=(0,50), pady=5)
        
        self.entryPoint = ctk.CTkEntry(containerEntry, corner_radius=3, border_color='#F4EEFF', fg_color='transparent', text_color='#F4EEFF', width=256, border_width=1)
        self.entryPoint.pack(side='left', pady=5)
        
        containerOut = ctk.CTkFrame(frame, fg_color='transparent')
        containerOut.pack()
        
        labelOut = ctk.CTkLabel(containerOut, text='Output File', text_color='#F4EEFF')
        labelOut.pack(side='left', padx=(0,40), pady=5)
        
        self.outPoint = ctk.CTkEntry(containerOut, corner_radius=3, border_color='#ecf0f1', border_width=1, text_color='#F4EEFF', fg_color='transparent', width=256)
        self.outPoint.pack(side='left', pady=5)
        
        containerKey = ctk.CTkFrame(frame, fg_color='transparent')
        containerKey.pack()
        
        labelKey = ctk.CTkLabel(containerKey, text='Key', text_color='#F4EEFF')
        labelKey.pack(side='left', padx=(15,0), pady=5)
        
        self.keyPoint = ctk.CTkEntry(containerKey, corner_radius=3, border_color='#F4EEFF', fg_color='transparent', text_color='#F4EEFF', width=256, border_width=1)
        self.keyPoint.pack(side='left', padx=(65, 0), pady=5)
        
        containerButton = ctk.CTkFrame(frame, fg_color='transparent')
        containerButton.pack()
        
        encryptButton = ctk.CTkButton(containerButton, text='Encrypt', text_color='#ecf0f1', fg_color='transparent', hover_color='#34495e', border_color='#ecf0f1', border_width=1, corner_radius=3, command=lambda: self.encryptFile(self.entryPoint.get(), self.outPoint.get()))
        encryptButton.pack(side='left', padx=35, pady=15)
        
        decryptButton = ctk.CTkButton(containerButton, text='Decrypt', text_color='#ecf0f1', fg_color='transparent', hover_color='#34495e', border_color='#ecf0f1', border_width=1, corner_radius=3, command=lambda: self.decryptFile(self.entryPoint.get(), self.outPoint.get(), self.keyPoint.get()))
        decryptButton.pack(side='left', padx=35, pady=15)

        self.displayError = ctk.CTkLabel(frame, text='')
        self.displayError.pack(pady=(10,0))
        
        window.mainloop()
        
    def encryptFile(self, path, output):
        def _encryption():
            try:
                key = Fernet.generate_key()
                cipher = Fernet(key)
                
                getPath = path
                getDirectory = output
                getVar = os.path.basename(getPath)
                getFilename = os.path.splitext(getVar)[0]
                
                if not os.path.isdir(getDirectory):
                    self.displayError.configure(text=f"Expected a directory.", text_color='#e74c3c')
                    return
                
                keyPath = os.path.join(getDirectory, f"{getFilename}.key")
                with open(keyPath, 'wb') as value_key:
                    value_key.write(key)
                    
                with open(getPath, 'rb') as content:
                    original = content.read()
                encrypted_file = cipher.encrypt(original)
                
                
                encryptedPath = os.path.join(getDirectory, f"[_enc_]{getVar}")
                with open(encryptedPath, 'wb') as got_encrypted:
                    got_encrypted.write(encrypted_file)
                
                self.displayError.configure(text='Encryption Successful.', text_color='#2ecc71')
            except Exception as e:
                self.displayError.configure(text=str(e), text_color='#e74c3c')
        threading.Thread(target=_encryption, daemon=True).start()

            
    def decryptFile(self, path, output, key):  
        def _decryption():
            try:      
                getPath = path
                getDirectory = output
                getKey = key
                getVar = os.path.basename(getPath)
                
                if not os.path.isdir(getDirectory):
                    self.displayError.configure(text=f"Expected a directory.", text_color='#e74c3c')
                    return
                if not os.path.isfile(getKey):
                    self.displayError.configure(text=f"Expected a file with extension [.key].", text_color='#e74c3c')
                    return
                if not getKey.endswith('.key'):
                    self.displayError.configure(text=f"Expected a file with extension [.key].", text_color='#e74c3c')
                    return

                with open(getKey, 'rb') as read_value_key:
                    unlocker = read_value_key.read()
                cipher = Fernet(unlocker)
                
                with open(getPath, 'rb') as content:
                    encrypted_content = content.read()
                    
                decrypt_file = cipher.decrypt(encrypted_content)
                clearEncrypted = getVar.replace("[_enc_]", "")
                decryptedPath = os.path.join(getDirectory, clearEncrypted)
                
                with open(decryptedPath, 'wb') as got_decrypted:
                    got_decrypted.write(decrypt_file)
                    
                self.displayError.configure(text='Decryption Successful.', text_color='#2ecc71')
            except Exception as e:
                self.displayError.configure(text=str(e), text_color='#e74c3c')
        threading.Thread(target=_decryption, daemon=True).start()

    def optionHandlerMenu(self):
        containerMenu = ctk.CTkFrame(self.frame, corner_radius=0, height=72)
        containerMenu.pack_propagate(False)
        containerMenu.pack(fill='x')
        
        containerOptions = ctk.CTkFrame(containerMenu, fg_color='#34495e', corner_radius=0, height=96)
        containerOptions.pack(fill='x')
        
        load_image = Image.open("./images/conversion.png")
        imageConversion = ctk.CTkImage(dark_image=load_image, light_image=load_image, size=(32,32))
        
        buttonConvertionFile = ctk.CTkButton(containerOptions, fg_color='#34495e', hover_color='#34495e', height=32, width=32, image=imageConversion, text='', corner_radius=0, command=self.handlerConverter)
        buttonConvertionFile.pack(side='left')
        
        load_image = Image.open("./images/download.png")
        imageDonwload = ctk.CTkImage(dark_image=load_image, light_image=load_image, size=(32,32))
        
        buttonDownload = ctk.CTkButton(containerOptions, fg_color='#34495e', hover_color='#34495e', height=32, width=32, image=imageDonwload, text='', corner_radius=0, command=self.handlerDownloader)
        buttonDownload.pack(side='left')
        
        load_image = Image.open("./images/encryption.png")
        imageEncryption = ctk.CTkImage(dark_image=load_image, light_image=load_image, size=(32,32))
        
        buttonEncryption = ctk.CTkButton(containerOptions, fg_color='#34495e', hover_color='#34495e', height=32, width=32, image=imageEncryption, text='', corner_radius=0, command=self.handlerEncrypter)
        buttonEncryption.pack(side='left')
        
        ToolTip(buttonConvertionFile, "It convert any format file to what it is available")
        ToolTip(buttonDownload, "It only download from youtube")
        ToolTip(buttonEncryption, "It encrypt and it decrypt the file")
        
        containerOptionsNavigation = ctk.CTkFrame(containerMenu, corner_radius=0, height=32)
        containerOptionsNavigation.pack(fill='x')

        containerAction = ctk.CTkFrame(containerOptionsNavigation, corner_radius=0, fg_color='#2c3e50')
        containerAction.pack(fill='x', side='left', expand=True)
        
        buttonArrowBack = ctk.CTkButton(containerAction, fg_color='#2c3e50', text='←', text_color='#F4EEFF', hover_color='#34495e', corner_radius=5, height=32, width=32, command=lambda: self.goBack())
        buttonArrowBack.configure(cursor="hand2")
        buttonArrowBack.pack(side="left", pady=(5,0), padx=(5,5))

        buttonArrowFoward = ctk.CTkButton(containerAction, fg_color='#2c3e50', text='→', text_color='#F4EEFF', hover_color='#34495e', corner_radius=5, height=32, width=32, command=lambda: self.visitBack())
        buttonArrowFoward.configure(cursor="hand2")
        buttonArrowFoward.pack(side="left", pady=(5,0))
        
        self.containerPath = ctk.CTkEntry(containerAction, fg_color='#2c3e50', text_color='#F4EEFF', border_color='#ecf0f1', border_width=1, corner_radius=0, height=32)
        self.containerPath.pack(side='left', fill='x', expand=True, padx=(5, 0), pady=(5,0))
        self.containerPath.insert(0, self.current_path)
        
        def getPath(event):
            self.current_path = self.containerPath.get()
            print(self.current_path)
            if self.current_path:
                if os.path.isdir(self.current_path):
                    os.chdir(self.current_path)
                    self.containerPath.delete(0, 'end')
                    self.containerPath.insert(0, os.getcwd())
                    self.listEverything()
                else:
                    messagebox.showerror('Error', 'The path does not exist or invalid')
        self.containerPath.bind("<Return>", getPath)
        self.listEverything()
        
        self.containerSearch = ctk.CTkEntry(containerAction, fg_color='#2c3e50', border_color='#ecf0f1', text_color='#F4EEFF', border_width=1, corner_radius=0, height=32, width=200)
        self.containerSearch.pack(side='left', padx=(5, 0), pady=(5,0))
        self.containerSearch.bind("<Return>", self.searchPath)
    
    def searchPath(self, event):
        def _search():
            value = self.containerSearch.get()
            
            if getattr(sys, 'frozen', False):
                project_dir = os.path.dirname(sys.executable)
            else:
                project_dir = os.path.dirname(os.path.abspath(__file__))
                
            directory_output = os.path.join(project_dir, 'logs')     
            if not os.path.exists(directory_output):
                os.mkdir(directory_output)
                
            file_output = os.path.join(directory_output, "search_result.txt")

            command = f'cmd /c "dir {self.current_path} /S | findstr /C:\"{value}\""'
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
                        
            if result.stdout:
                with open(file_output, "w") as file:
                    file.write(result.stdout)

                messagebox.showinfo('Success', 'The search has completely found, check on the logs')    
            else:
                messagebox.showerror('Error', 'File or directory not found')

                                    
        threading.Thread(target=_search, daemon=True).start()

    def quickHandlerAccess(self):
        self.containerQuickAccess = ctk.CTkScrollableFrame(self.frame, fg_color='#2c3e50', scrollbar_button_color='#ecf0f1', scrollbar_button_hover_color='#ecf0f1', corner_radius=0, width=256)
        self.containerQuickAccess.pack(fill='both', side='left', pady=5)
        
        self.initShortcut()

    def menuHandlerContent(self):
        self.containerContent.pack(fill='both', side='right', expand=True, pady=5)

    def getFileCreated(self, filedata):
        getData = os.path.getctime(filedata)
        formatData = time.strftime('%d/%m/%Y %I:%M:%S %p', time.localtime(getData))
        
        return formatData
    
    def getFileSize(self, filesize):
        getSize = os.path.getsize(filesize)
        size_units = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
        
        index = 0
        if getSize == 0:
            return ''
        else:
            while getSize >= 1024 and index < len(size_units) - 1:
                getSize /= 1024.0
                index += 1
            return f"{getSize:.2f} {size_units[index]}"
        
    def listEverything(self):
        try:
            if hasattr(self, "content_labels"):
                for label in self.content_labels:
                    label.destroy()
            self.content_labels = []  
            content = os.listdir(self.current_path)
            header = ['Name', 'Data Created', 'Size', 'Status']
            
            containerHeader = ctk.CTkFrame(self.containerContent, fg_color="#34495e")
            containerHeader.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=1)

            for col in range(4):
                containerHeader.grid_columnconfigure(col, weight=1)
                
            for col in range(4):
                self.containerContent.grid_columnconfigure(col, weight=1)

            for col, text in enumerate(header):
                header_label = ctk.CTkLabel(containerHeader, text=text, text_color="#2c3e50", anchor="center")
                header_label.grid(row=0, column=col, sticky="nsew")
                containerHeader.configure(fg_color="#ecf0f1")
            
            for row, item in enumerate(content, start=1):
                item_path = os.path.join(self.current_path, item)
                
                filename = item
                filecreation = self.getFileCreated(item_path)
                filesize = self.getFileSize(item_path)
                
                if os.path.isdir(os.path.join(self.current_path, item)):
                    name_label = ctk.CTkLabel(containerHeader, text=f'📁 {filename}', fg_color="#34495e", text_color="#ecf0f1", anchor="w")
                    name_label.bind('<Double-1>', lambda event, path=item: self.goFoward(path))
                elif os.path.isfile(os.path.join(self.current_path, item)):
                    name_label = ctk.CTkLabel(containerHeader, text=f'📄 {filename}', fg_color="#34495e", text_color="#ecf0f1", anchor="w")
                    name_label.bind('<Double-1>', lambda event, file=item: self.executeFile(file))
                
                name_label.grid(row=row, column=0, sticky="nsew")
                name_label.configure(cursor='hand2')
                
                date_label = ctk.CTkLabel(containerHeader, text=filecreation, fg_color="#34495e", text_color="#ecf0f1", anchor="center")
                date_label.grid(row=row, column=1, sticky='nsew')
                
                size_label = ctk.CTkLabel(containerHeader, text=filesize, fg_color="#34495e", text_color="#ecf0f1", anchor="center")
                size_label.grid(row=row, column=2, sticky='nsew')
                
                status_label = ctk.CTkLabel(containerHeader, text=None, fg_color="#34495e", text_color="#ecf0f1", anchor="center")
                status_label.grid(row=row, column=3, sticky='nsew')

                labels = [label for label in [name_label, date_label, size_label, status_label]]

                for label in labels:
                    label.bind('<Enter>', lambda event, labels=labels: [label.configure(fg_color='#ecf0f1', text_color="#2c3e50") for label in labels])
                    label.bind('<Leave>', lambda event, labels=labels: [label.configure(fg_color='#34495e', text_color="#ecf0f1") for label in labels])
                
                self.content_labels.extend(labels)
        except Exception as e:
            containerHeader = ctk.CTkFrame(self.containerContent, fg_color="#34495e")
            containerHeader.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=1)

            for col in range(4):
                containerHeader.grid_columnconfigure(col, weight=1)
                
            for col in range(4):
                self.containerContent.grid_columnconfigure(col, weight=1)
                
            self.displayError = ctk.CTkLabel(containerHeader, text=str(e), text_color='#e74c3c')
            self.displayError.grid(pady=5, columnspan=4)    
    
    def initShortcut(self):
        content = ['Desktop', 'Documents', 'Downloads', 'Music', 'Pictures', 'Videos']
        if os.name == 'nt':
            for row, item in enumerate(content, start=1):
                label = ctk.CTkLabel(self.containerQuickAccess, text=f'📁 {item}', fg_color="#34495e", text_color="#ecf0f1", anchor="w", corner_radius=5)
                label.grid(row=row, column=0, sticky='nsew', pady=1)

                label.bind('<Double-1>', lambda event, shortcut=item: self.getShortcut(shortcut))
                
                def change_color_enter(event, label=label):
                    label.configure(fg_color='#ecf0f1', text_color="#2c3e50")

                def change_color_leave(event, label=label):
                    label.configure(fg_color='#34495e', text_color="#ecf0f1")

                label.bind('<Enter>', change_color_enter)
                label.bind('<Leave>', change_color_leave)

                self.containerQuickAccess.grid_columnconfigure(0, weight=1)
                label.configure(cursor='hand2')
    
    def getShortcut(self, shortcut):
        gotShortcut = os.path.join(os.getenv('USERPROFILE'), shortcut)
        
        self.current_path = gotShortcut
        os.chdir(self.current_path)
        
        if not self.history or self.history[-1] != self.current_path:
            self.history.append(self.current_path)
            self.popped_history.clear()
        
        self.listEverything()
        self.containerPath.delete(0, 'end')
        self.containerPath.insert(0, self.current_path)
        self.validateHistory()

    def goFoward(self, path):
        new_path = os.path.join(self.current_path, path)
        if os.path.isdir(new_path):
            if not self.history or self.history[-1] != new_path:
                self.history.append(new_path)
                print(self.history)
                
            os.chdir(new_path)
            self.current_path = os.getcwd()
            self.popped_history.clear()
            
            self.containerPath.delete(0, 'end')
            self.containerPath.insert(0, self.current_path)
            
            self.listEverything()   
            self.validateHistory()
        print(self.history, '\n', self.popped_history)
    
    def goBack(self):               
        if len(self.history) > 1:
            last_path = self.history.pop()
            self.popped_history.append(last_path)
            path = self.history[-1]
            os.chdir(path)
            self.current_path = os.getcwd()
            
            self.containerPath.delete(0, 'end')
            self.containerPath.insert(0, self.current_path)
            
            self.listEverything()
            self.validateHistory()
        print(self.history, '\n', self.popped_history)
       
    def visitBack(self):
        if self.popped_history:
            next_path = self.popped_history.pop()
            self.history.append(next_path)
            self.current_path = next_path
            os.chdir(self.current_path)
            
            self.containerPath.delete(0, 'end')
            self.containerPath.insert(0, self.current_path)
            
            self.listEverything()
            self.validateHistory()
        print(self.history, '\n', self.popped_history)
        
    def validateHistory(self):
        if self.current_path not in self.history:
            valid_history = []
            for path in self.history:
                if os.path.commonpath([path, self.current_path]) == path:
                    valid_history.append(path)
                else:
                    break
            self.history = valid_history
            print("Adjusted History:", self.history)
            
    def executeFile(self, file):
        os.chdir(self.current_path)
        os.startfile(file)
        
    def initLayout(self):        
        self.current_path = 'C:\\' if os.name == 'nt' else '/'
        self.history.append('C:\\') if os.name == 'nt' else self.history.append('/')
        self.containerContent = ctk.CTkScrollableFrame(self.frame, fg_color='#2c3e50', scrollbar_button_color='#ecf0f1', scrollbar_button_hover_color='#ecf0f1', corner_radius=0)
        self.content_labels = []
        
        self.optionHandlerMenu()
        self.quickHandlerAccess()
        self.menuHandlerContent()
    
Interface()