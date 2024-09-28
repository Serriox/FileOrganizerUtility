import tkinter.messagebox
import shutil
import os
import json

import customtkinter


customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("FileOrganizerUtility")
        self.iconbitmap("icon.ico")
        self.geometry("800x600")
        self.resizable(False, False)
        
        
        self.grid_rowconfigure(
            index = 0,
            weight = 1
        )
        self.grid_columnconfigure(
            index = 1,
            weight = 1
        )
        
        
        self.sidebar_frame = customtkinter.CTkFrame(
            master = self,
            height = 600,
            corner_radius = 0
        )
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.title_label = customtkinter.CTkLabel(
            master = self.sidebar_frame,
            text = "FileOrganizer\nUTILITY",
            font = customtkinter.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=24, pady=24)
        
        
        self.frame = customtkinter.CTkFrame(
            master = self,
            width = 512,
            height = 256
        )
        self.frame.grid(row=0, column=1, padx=32, pady=32, sticky="nsew")
        
        
        self.path_label = customtkinter.CTkLabel(
            master = self.frame,
            text = "Path",
            font = customtkinter.CTkFont(size=20)
        )
        self.path_label.grid(row=0, column=0, padx=8, pady=8)
        
        self.path_setting = customtkinter.CTkEntry(
            master = self.frame,
            width = 512,
            placeholder_text = "Insert path where files should be organized",
            font = customtkinter.CTkFont(size=16)
        )
        self.path_setting.grid(row=1, column=0, padx=8, pady=8)
        
        
        self.config_label = customtkinter.CTkLabel(
            master = self.frame,
            text = "Configuration\n(only edit this if you know what you are doing!)",
            font = customtkinter.CTkFont(size=20)
        )
        self.config_label.grid(row=2, column=0, padx=8, pady=(32, 8))
        
        self.config_setting = customtkinter.CTkTextbox(
            master = self.frame,
            width = 512,
            height = 256,
            font = customtkinter.CTkFont(size=16)
        )
        
        with open(f"config.json", "rb") as cfg:
            self.config_setting.insert("0.0", cfg.read())
        
        self.config_setting.grid(row=3, column=0, padx=8, pady=8)
        
        self.save_button = customtkinter.CTkButton(
            master = self.frame,
            text = "Save configuration",
            font = customtkinter.CTkFont(size=16),
            command = lambda: self.save_config(self.config_setting.get("0.0", customtkinter.END))
        )
        self.save_button.grid(row=4, column=0, padx=8, pady=8)
        

        self.organize_button = customtkinter.CTkButton(
            master = self.frame,
            text = "ORGANIZE",
            font = customtkinter.CTkFont(size=16),
            command = lambda: self.organize_files(self.path_setting.get())
        )
        self.organize_button.grid(row=5, column=0, padx=8, pady=8)
    
    
    def save_config(self, new_cfg):
        try:
            os.remove("config.json")
            
            with open("config.json", "w") as cfg:
                cfg.write(new_cfg)
            
            tkinter.messagebox.showinfo(
                title = "Info",
                message = "Successfully saved configuration"
            )
        except Exception:
            tkinter.messagebox.showerror(
                title = "Error",
                message = "Unknown error"
            )

            return
    
    def organize_files(self, path):
        with open("config.json", "r") as cfg:
            self.cfg_data = dict(json.load(cfg))
        
        for file in os.listdir(path):
            file_format = os.path.splitext(file)[1].lower()
            
            for folder in self.cfg_data:
                for file_type in self.cfg_data[folder]:
                    if file.endswith(file_format) and file_format == file_type:
                        os.system(f"mkdir {path}\\{folder}")
                        shutil.move(f"{path}\\{file}", f"{path}\\{folder}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
