import platform
import subprocess
import time
import os
from colorama import Fore, Style, init

init(autoreset=True)

class WiFiIntrusionProtocol:
    def __init__(self):
        self.system_name = platform.system()
        self.accessible_networks = []
        self.load_networks()

    def load_networks(self):
        try:
            if self.system_name == "Windows":
                self.accessible_networks = self.retrieve_networks_windows()
            elif self.system_name == "Linux":
                self.accessible_networks = self.retrieve_networks_linux()
            elif self.system_name == "Darwin":
                self.accessible_networks = self.retrieve_networks_mac()
        except subprocess.CalledProcessError:
            self.accessible_networks = []

    def retrieve_networks_windows(self):
        output = subprocess.check_output("netsh wlan show profiles", shell=True, text=True)
        return [line.split(":")[1].strip() for line in output.splitlines() if "All User Profile" in line]

    def retrieve_networks_linux(self):
        output = subprocess.check_output("ls /etc/NetworkManager/system-connections", shell=True, text=True)
        return output.splitlines()

    def retrieve_networks_mac(self):
        output = subprocess.check_output("security find-generic-password -l", shell=True, text=True)
        return [line.strip() for line in output.splitlines()]

    def obtain_password_windows(self, network_name):
        output = subprocess.check_output(f"netsh wlan show profile \"{network_name}\" key=clear", shell=True, text=True)
        key_content = [line.split(":")[1].strip() for line in output.splitlines() if "Key Content" in line]
        if key_content:
            return key_content[0]
        else:
            return "No password found for the network"

    def obtain_password_linux(self, network_name):
        output = subprocess.check_output(f"cat /etc/NetworkManager/system-connections/{network_name}", shell=True, text=True)
        psk_content = [line.split("=")[1].strip() for line in output.splitlines() if line.startswith("psk")]
        if psk_content:
            return psk_content[0]
        else:
            return "No password found for the network"

    def obtain_password_mac(self, network_name):
        output = subprocess.check_output(f"security find-generic-password -wa {network_name}", shell=True, text=True)
        password = output.strip()
        if password:
            return password
        else:
            return "No password found for the network"

    def display_title(self, title):
        print(f"{Fore.CYAN}{Style.BRIGHT}{title}{Style.RESET_ALL}")

    def display_warning(self, message):
        print(f"{Fore.YELLOW}{Style.BRIGHT}{message}{Style.RESET_ALL}")

    def display_error(self, message):
        print(f"{Fore.RED}{Style.BRIGHT}{message}{Style.RESET_ALL}")

    def display_success(self, message):
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

    def save_networks_to_file(self):
        filename = f"wireless_infiltration_data_{self.system_name.lower()}.txt"
        with open(filename, "a") as f:
            f.write("\n" + "=" * 60 + "\n")
            f.write(f"{'Wireless Networks':^60}\n")
            f.write("=" * 60 + "\n")
            f.write(f"{'Platform:':<20} {self.system_name}\n")
            f.write("=" * 60 + "\n\n")
            for network in self.accessible_networks:
                f.write(f"Network: {network}\n")
                if self.system_name == "Windows":
                    password = self.obtain_password_windows(network)
                elif self.system_name == "Linux":
                    password = self.obtain_password_linux(network)
                elif self.system_name == "Darwin":
                    password = self.obtain_password_mac(network)
                f.write(f"Password: {password}\n\n")
        self.display_success(f"{Style.BRIGHT} Passwords have been discreetly added to {filename}{Style.RESET_ALL}\n")

    def show_networks(self):
        print(f"{Fore.CYAN}{Style.BRIGHT}Identified target networks:{Style.RESET_ALL}")
        for idx, network in enumerate(self.accessible_networks, start=1):
            print(f"{Fore.YELLOW}{idx}.{Style.RESET_ALL} {network}")
        print(f"{Fore.YELLOW}\n0.{Style.RESET_ALL} {Style.BRIGHT}{Fore.MAGENTA}Advanced Options")

    def obtain_password(self, network_name):
        if self.system_name == "Windows":
            return self.obtain_password_windows(network_name)
        elif self.system_name == "Linux":
            return self.obtain_password_linux(network_name)
        elif self.system_name == "Darwin":
            return self.obtain_password_mac(network_name)

    def animate_typing(self, text, delay=0.02, color=Fore.RESET):
        for char in text:
            print(f"{color}{char}{Style.RESET_ALL}", end='', flush=True)
            time.sleep(delay)
        print()

    def display_loading(self, message):
        print(f"{Fore.CYAN}{Style.BRIGHT}{message}{Style.RESET_ALL}", end="")

    def initiate_protocol(self):
        self.display_loading("Initiating protocol:")
        self.save_networks_to_file()

    def advanced_option(self):
        print(f"\n{Fore.CYAN}Advanced Options:\n{Fore.YELLOW}1.{Style.RESET_ALL} Download Additional Data")
        print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Analyze Data")
        choice = input(f"\n{Fore.CYAN}Select an option (1/2): ")
        if choice == "1":
            self.download_additional_data()
        elif choice == "2":
            self.analyze_data()
        else:
            self.display_warning(f"{Style.BRIGHT}Invalid option. Returning to main menu.{Style.RESET_ALL}")

    def download_additional_data(self):
        print(f"\n{Fore.CYAN}Downloading additional data:")
        for _ in range(3):
            self.display_loading(".")
            time.sleep(1)
        print(f"\n{Fore.GREEN}{Style.BRIGHT}Additional data successfully downloaded.\n{Style.RESET_ALL}")

    def analyze_data(self):
        print(f"\n{Fore.CYAN}Analyzing data:")
        for _ in range(3):
            self.display_loading(".")
            time.sleep(1)
        print(f"\n{Fore.GREEN}{Style.BRIGHT}Analysis complete. No security threats detected.\n{Style.RESET_ALL}")

    def execute(self):
        self.display_titles()

        if not self.accessible_networks:
            self.display_error(f"{Style.BRIGHT}No target systems detected. Terminating...{Style.RESET_ALL}")
            return

        while True:
            self.show_networks()
            choice = input(f"\n{Fore.CYAN}Initiate protocol {Fore.YELLOW}{Style.BRIGHT}A{Style.RESET_ALL} (auto mode), {Fore.RED}{Style.BRIGHT}Q{Style.RESET_ALL} (quit), or select a network (1-{len(self.accessible_networks)}): ")
            if choice.lower() == "a":
                self.show_loading_animation("Initiating protocol")
                self.initiate_protocol()
            elif choice.isdigit():
                network_choice = int(choice) - 1
                if network_choice == -1:
                    self.advanced_option()
                elif 0 <= network_choice < len(self.accessible_networks):
                    chosen_network = self.accessible_networks[network_choice]
                    loading_message = f"Infiltrating target {chosen_network}"
                    self.show_loading_animation(loading_message)
                    password = self.obtain_password(chosen_network)
                    self.display_success(f"{Style.RESET_ALL}Target {Fore.RED}{Style.BRIGHT}#{network_choice + 1} {Style.RESET_ALL}infiltrated. {Fore.YELLOW}Data retrieved:{Style.BRIGHT} {Fore.GREEN}{password}{Style.RESET_ALL}\n")
                    self.return_option()
                else:
                    self.display_warning(f"{Style.BRIGHT}\nIntrusion failed. Network compromised.{Style.RESET_ALL}\n")
            elif choice.lower() == "q":
                self.display_success(f"{Fore.CYAN}Exiting the infiltration protocol. Operation concluded.{Style.RESET_ALL}")
                break
            else:
                self.display_warning(f"{Style.BRIGHT}\nInvalid command. Reevaluate input.{Style.RESET_ALL}\n")

    def display_titles(self):
        self.animate_typing("Wireless Infiltration Security Protocol", color=Fore.CYAN + Style.BRIGHT)
        self.animate_typing("Developed by Angelo Manalo\n", color=Fore.GREEN + Style.BRIGHT)

    def return_option(self):
        input(f"{Fore.YELLOW}Press Enter to return to the main menu...{Style.RESET_ALL}")
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_titles()
        print()

    def show_loading_animation(self, message, delay=0.1, iterations=3):
        animation_chars = ["|", "/", "-", "\\"]
        for _ in range(iterations):
            for char in animation_chars:
                print(f"\r{Fore.CYAN}{Style.BRIGHT}{message}{Style.RESET_ALL} {char}", end="")
                time.sleep(delay)
        print("\r", end="")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    protocol = WiFiIntrusionProtocol()
    protocol.execute()
    time.sleep(2)
