import customtkinter
import json
import shutil
import os

class Window(customtkinter.CTk):

    def __init__(self):  
        super().__init__()

        self.title("UISwap")
        self.geometry(f"{800}x{500}")

        customtkinter.set_appearance_mode(profilesSettings["apperance_mode"])
        customtkinter.set_default_color_theme(profilesSettings["color_mode"])
        customtkinter.set_widget_scaling(
            int(profilesSettings["scaling_event"].replace("%", "")) / 100)
        
        self.grid_columnconfigure((1, 2, 3), weight=0)
        self.grid_rowconfigure((1, 2), weight=0)
        
        # create widgets        
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="UISwap", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.buttonGamePath = customtkinter.CTkButton(self.sidebar_frame, text="Path to game", command=self.game_path)
        self.buttonGamePath.grid(row=4, column=0, padx=20, pady=(10, 10))
        
        self.color_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Color Mode:", anchor="w")
        self.color_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.color_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["blue", "green", "dark-blue"],
                                                                       command=self.change_color_mode_event)
        self.color_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(5, 5))
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(5, 5))
        
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(5, 25))

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=2, padx=(5, 5), pady=(5, 5), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew")
        self.tabviewDictEntry = {}
        for profile in profilesSettings["profiles"]:            
            self.createTabview(profile)
        
        #create buttons     
        self.newProfile = customtkinter.CTkButton(self, text="New Profile", command=self.new_profile)
        self.newProfile.grid(row=1, column=1, padx=20, pady=(10, 10))
        self.buttonSave = customtkinter.CTkButton(self, text="Save", command=self.save_chages)
        self.buttonSave.grid(row=1, column=2, padx=20, pady=(10, 10))
        
        # set default values
        self.appearance_mode_optionemenu.set(profilesSettings["apperance_mode"])
        self.scaling_optionemenu.set(profilesSettings["scaling_event"])
        self.color_mode_optionemenu.set(profilesSettings["color_mode"])
        self.textbox.insert("0.0", profilesSettings["textbox"])

        self.mainloop()


    def createTabview(self, profile: str):
        self.tabview.add(profile)
        self.tabview.tab(profile).grid_columnconfigure(0, weight=1) 
        self.tabviewDictEntry[profile] = {'copy': None, 'inserts': None}

        customtkinter.CTkButton(master=self.tabview.tab(profile), border_width=2, text_color=("gray10", "#DCE4EE"), text='Activate profile', 
                                command= lambda profile=profile: self.profileActivation(profile)).grid(
            row=0, column=0, padx=(100, 100), pady=(20, 20), sticky="nsew")       

        self.tabviewDictEntry[profile] = {'copy': customtkinter.CTkEntry(self.tabview.tab(profile), placeholder_text=profilesSettings["profiles"][profile]["copy"]),
                                        'inserts': customtkinter.CTkEntry(self.tabview.tab(profile), placeholder_text=profilesSettings["profiles"][profile]["inserts"])}
        self.tabviewDictEntry[profile]['copy'].grid(row=1, column=0, columnspan=1, padx=(5, 5), pady=(20, 2), sticky="nsew")
        self.tabviewDictEntry[profile]['inserts'].grid(row=3, column=0, columnspan=1, padx=(5, 5), pady=(20, 2), sticky="nsew")
        
        customtkinter.CTkButton(master=self.tabview.tab(profile), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='New path (copy)', 
                                command= lambda profile=profile: self.swapPathCopy(profile, self.tabviewDictEntry[profile]['copy'].get())).grid(
            row=2, column=0, padx=(100, 100), pady=(2, 20), sticky="nsew")
        
        customtkinter.CTkButton(master=self.tabview.tab(profile), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='New path (inserts)', 
                                command=lambda profile=profile: self.swapPathInserts(profile, self.tabviewDictEntry[profile]['inserts'].get())).grid(
            row=4, column=0, padx=(100, 100), pady=(2, 20), sticky="nsew")
    
        customtkinter.CTkButton(master=self.tabview.tab(profile), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Delete profile', 
                                command=lambda profile=profile: self.deleteProfile(profile)).grid(
            row=5, column=0, padx=(100, 100), pady=(50, 20), sticky="nsew") 


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
    def change_color_mode_event(self, new_color_mode: str):
        profilesSettings["color_mode"] = new_color_mode
        self.destroy()
        Window()

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def new_profile(self):
        dialog = customtkinter.CTkInputDialog(text="Profile name", title="New Profile")
        profile = dialog.get_input()
        if profile is not None and profile not in profilesSettings['profiles']:
            profilesSettings['profiles'][profile] = {'copy': 'path_copy', 'inserts': 'path_inserts'}
            self.createTabview(profile)
            
    def game_path(self):
        dialog = customtkinter.CTkInputDialog(text="Path to game", title="Settings")
        path = dialog.get_input()
        if path is not None:
            profilesSettings['path_game'] = path
        
    def save_chages(self):
        profilesSettings['textbox'] = self.textbox.get("0.0", 'end')
        with open("settings.json", "w") as f:
            json.dump(profilesSettings, f, indent=2)
            
    def deleteProfile(self, profile: str):
        profilesSettings['profiles'].pop(profile)
        self.tabview.delete(profile)
        
    def swapPathCopy(self, profile: str, path: str):
        profilesSettings['profiles'][profile]['copy'] = path
        self.tabviewDictEntry[profile]['copy'].configure(placeholder_text=path)
    
    def swapPathInserts(self, profile: str, path: str):
        profilesSettings['profiles'][profile]['inserts'] = path
        self.tabviewDictEntry[profile]['inserts'].configure(placeholder_text=path)
    
    def profileActivation(self, profile):
        try:
            shutil.copy(profilesSettings['profiles'][profile]['copy'], profilesSettings['profiles'][profile]['inserts'])
            os.startfile(profilesSettings['path_game'])
        except: 
            self.tabviewDictEntry[profile]['copy'].configure(placeholder_text='Error!')
            self.tabviewDictEntry[profile]['inserts'].configure(placeholder_text='Error!')
            self.textbox.insert("0.0", f'{"-"*15}\n\n\n!!!!! ERROR - bad path\n\n\n{"-"*15}\n')
    
if __name__ == '__main__':
    with open('settings.json') as f:
        profilesSettings = json.load(f)
    
    Window()

    
        
