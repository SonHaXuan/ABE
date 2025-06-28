'''
System Information Collection Script
Collects hardware and software configuration details for research documentation
Author: System Analysis Tool
Date: Generated for ABE Performance Study
'''

import platform
import psutil
import subprocess
import sys
import os
import csv
from datetime import datetime

class SystemInfoCollector:
    def __init__(self):
        self.system_info = {}
        self.collect_all_info()
    
    def get_cpu_info(self):
        """Collect CPU information"""
        try:
            # Get CPU brand/model
            if platform.system() == "Darwin":  # macOS
                cpu_brand = subprocess.check_output(
                    ["sysctl", "-n", "machdep.cpu.brand_string"]
                ).decode().strip()
            elif platform.system() == "Linux":
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "model name" in line:
                            cpu_brand = line.split(":")[1].strip()
                            break
                    else:
                        cpu_brand = "Unknown"
            else:  # Windows
                cpu_brand = platform.processor()
            
            return {
                'brand': cpu_brand,
                'architecture': platform.machine(),
                'cores_physical': psutil.cpu_count(logical=False),
                'cores_logical': psutil.cpu_count(logical=True),
                'frequency_ghz': round(psutil.cpu_freq().max / 1000, 2) if psutil.cpu_freq() else "Unknown"
            }
        except Exception as e:
            return {
                'brand': f"Error collecting CPU info: {str(e)}",
                'architecture': platform.machine(),
                'cores_physical': psutil.cpu_count(logical=False),
                'cores_logical': psutil.cpu_count(logical=True),
                'frequency_ghz': "Unknown"
            }
    
    def get_memory_info(self):
        """Collect memory information"""
        memory = psutil.virtual_memory()
        return {
            'total_gb': round(memory.total / (1024**3), 2),
            'available_gb': round(memory.available / (1024**3), 2),
            'type': self.get_memory_type()
        }
    
    def get_memory_type(self):
        """Try to determine memory type"""
        try:
            if platform.system() == "Darwin":  # macOS
                result = subprocess.check_output(
                    ["system_profiler", "SPMemoryDataType"]
                ).decode()
                if "DDR4" in result:
                    return "DDR4"
                elif "DDR5" in result:
                    return "DDR5"
                elif "DDR3" in result:
                    return "DDR3"
                else:
                    return "Unknown DDR"
            else:
                return "Unknown"
        except:
            return "Unknown"
    
    def get_os_info(self):
        """Collect operating system information"""
        return {
            'name': platform.system(),
            'version': platform.version(),
            'release': platform.release(),
            'platform': platform.platform(),
            'python_version': platform.python_version()
        }
    
    def get_python_packages(self):
        """Get versions of key Python packages used in the project"""
        packages = {}
        
        # List of packages to check - enhanced with blockchain/IPFS tools
        key_packages = [
            'charm-crypto',
            'psutil',
            'numpy',
            'pandas',
            'cryptography',
            'pycryptodome',
            'web3',
            'ipfshttpclient',
            'ethereum',
            'py-evm',
            'eth-utils',
            'eth-keys',
            'requests',
            'flask',
            'solcx',
            'brownie-eth'
        ]
        
        for package in key_packages:
            try:
                result = subprocess.check_output([sys.executable, '-m', 'pip', 'show', package])
                lines = result.decode().split('\n')
                for line in lines:
                    if line.startswith('Version:'):
                        packages[package] = line.split(':')[1].strip()
                        break
                else:
                    packages[package] = "Not found"
            except:
                packages[package] = "Not installed"
        
        return packages

    def get_storage_info(self):
        """Get storage information"""
        try:
            disk_usage = psutil.disk_usage('/')
            return {
                'total_gb': round(disk_usage.total / (1024**3), 2),
                'free_gb': round(disk_usage.free / (1024**3), 2),
                'type': self.get_storage_type()
            }
        except:
            return {
                'total_gb': "Unknown",
                'free_gb': "Unknown",
                'type': "Unknown"
            }
    
    def get_storage_type(self):
        """Try to determine storage type (SSD/HDD)"""
        try:
            if platform.system() == "Darwin":  # macOS
                result = subprocess.check_output(
                    ["system_profiler", "SPStorageDataType"]
                ).decode()
                if "Solid State" in result or "SSD" in result:
                    return "SSD"
                else:
                    return "HDD/Unknown"
            else:
                return "Unknown"
        except:
            return "Unknown"

    def get_blockchain_tools(self):
        """Get blockchain and IPFS tool versions"""
        tools = {}
        
        # Check for Ganache CLI
        try:
            result = subprocess.check_output(['ganache-cli', '--version'], stderr=subprocess.STDOUT)
            tools['Ganache CLI'] = result.decode().strip().split('\n')[0]
        except:
            tools['Ganache CLI'] = "Not installed"
        
        # Check for Truffle
        try:
            result = subprocess.check_output(['truffle', 'version'], stderr=subprocess.STDOUT)
            lines = result.decode().split('\n')
            for line in lines:
                if 'Truffle' in line:
                    tools['Truffle'] = line.split(':')[1].strip() if ':' in line else line.strip()
                    break
            else:
                tools['Truffle'] = "Not found"
        except:
            tools['Truffle'] = "Not installed"
        
        # Check for IPFS
        try:
            result = subprocess.check_output(['ipfs', 'version'], stderr=subprocess.STDOUT)
            tools['IPFS'] = result.decode().strip()
        except:
            tools['IPFS'] = "Not installed"
        
        # Check for Go Ethereum (geth)
        try:
            result = subprocess.check_output(['geth', 'version'], stderr=subprocess.STDOUT)
            lines = result.decode().split('\n')
            for line in lines:
                if 'Version:' in line:
                    tools['Go Ethereum (geth)'] = line.split(':')[1].strip()
                    break
            else:
                tools['Go Ethereum (geth)'] = "Not found"
        except:
            tools['Go Ethereum (geth)'] = "Not installed"
        
        return tools

    def get_gpu_info(self):
        """Get GPU information if available"""
        try:
            if platform.system() == "Darwin":  # macOS
                result = subprocess.check_output(
                    ["system_profiler", "SPDisplaysDataType"]
                ).decode()
                # Extract GPU info
                lines = result.split('\n')
                gpu_info = "Unknown"
                for line in lines:
                    if "Chipset Model:" in line:
                        gpu_info = line.split(':')[1].strip()
                        break
                return gpu_info
            else:
                return "Unknown"
        except:
            return "Not detected"

    def get_network_info(self):
        """Get network interface information"""
        try:
            interfaces = psutil.net_if_addrs()
            active_interfaces = []
            for interface, addresses in interfaces.items():
                if interface not in ['lo', 'lo0']:  # Skip loopback
                    for addr in addresses:
                        if addr.family.name in ['AF_INET', 'AF_INET6']:
                            active_interfaces.append(interface)
                            break
            return ', '.join(active_interfaces[:3])  # Limit to first 3
        except:
            return "Unknown"

    def collect_all_info(self):
        """Collect all system information"""
        print("Collecting system information...")
        
        self.system_info = {
            'collection_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'os': self.get_os_info(),
            'storage': self.get_storage_info(),
            'packages': self.get_python_packages(),
            'blockchain_tools': self.get_blockchain_tools(),
            'gpu': self.get_gpu_info(),
            'network': self.get_network_info()
        }

    def generate_academic_table(self):
        """Generate academic-style configuration table"""
        print("\n" + "="*80)
        print("HARDWARE AND SOFTWARE CONFIGURATION TABLE")
        print("="*80)
        
        # Hardware Configuration
        print("\nHARDWARE CONFIGURATION:")
        print("-"*50)
        
        cpu = self.system_info['cpu']
        memory = self.system_info['memory']
        storage = self.system_info['storage']
        
        hardware_table = [
            ["Component", "Specification"],
            ["-"*20, "-"*40],
            ["Processor (CPU)", f"{cpu['brand']}"],
            ["Architecture", f"{cpu['architecture']}"],
            ["Physical Cores", f"{cpu['cores_physical']} cores"],
            ["Logical Cores", f"{cpu['cores_logical']} cores"],
            ["CPU Frequency", f"{cpu['frequency_ghz']} GHz" if cpu['frequency_ghz'] != "Unknown" else "Unknown"],
            ["Graphics (GPU)", f"{self.system_info['gpu']}"],
            ["Total RAM", f"{memory['total_gb']} GB"],
            ["Available RAM", f"{memory['available_gb']} GB"],
            ["Memory Type", f"{memory['type']}"],
            ["Storage Total", f"{storage['total_gb']} GB"],
            ["Storage Available", f"{storage['free_gb']} GB"],
            ["Storage Type", f"{storage['type']}"],
            ["Network Interfaces", f"{self.system_info['network']}"]
        ]
        
        for row in hardware_table:
            print(f"{row[0]:<20} | {row[1]}")
        
        # Software Configuration
        print("\nSOFTWARE CONFIGURATION:")
        print("-"*50)
        
        os_info = self.system_info['os']
        packages = self.system_info['packages']
        
        software_table = [
            ["Component", "Version/Details"],
            ["-"*20, "-"*40],
            ["Operating System", f"{os_info['name']} {os_info['release']}"],
            ["OS Platform", f"{os_info['platform']}"],
            ["Python Version", f"{os_info['python_version']}"],
            ["Charm-Crypto", f"{packages.get('charm-crypto', 'Not installed')}"],
            ["Psutil", f"{packages.get('psutil', 'Not installed')}"],
            ["Cryptography", f"{packages.get('cryptography', 'Not installed')}"],
            ["PyCryptodome", f"{packages.get('pycryptodome', 'Not installed')}"],
            ["Web3.py", f"{packages.get('web3', 'Not installed')}"],
            ["IPFS HTTP Client", f"{packages.get('ipfshttpclient', 'Not installed')}"],
            ["NumPy", f"{packages.get('numpy', 'Not installed')}"],
            ["Pandas", f"{packages.get('pandas', 'Not installed')}"]
        ]
        
        for row in software_table:
            print(f"{row[0]:<20} | {row[1]}")

        # Blockchain/IPFS Tools
        print("\nBLOCKCHAIN & IPFS TOOLS:")
        print("-"*50)
        
        blockchain_tools = self.system_info['blockchain_tools']
        
        blockchain_table = [
            ["Tool", "Version"],
            ["-"*20, "-"*40],
            ["IPFS", f"{blockchain_tools.get('IPFS', 'Not installed')}"],
            ["Ganache CLI", f"{blockchain_tools.get('Ganache CLI', 'Not installed')}"],
            ["Truffle", f"{blockchain_tools.get('Truffle', 'Not installed')}"],
            ["Go Ethereum", f"{blockchain_tools.get('Go Ethereum (geth)', 'Not installed')}"]
        ]
        
        for row in blockchain_table:
            print(f"{row[0]:<20} | {row[1]}")
        
        print(f"\nCollection Time: {self.system_info['collection_time']}")
        print("="*80)

    def export_to_csv(self, filename="system_configuration.csv"):
        """Export configuration to CSV format"""
        csv_path = f"/Users/thanhtuan/son/ABE/samples/{filename}"
        
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(["Configuration Type", "Component", "Specification"])
                
                # Hardware section
                cpu = self.system_info['cpu']
                memory = self.system_info['memory']
                storage = self.system_info['storage']
                
                hardware_rows = [
                    ["Hardware", "Processor (CPU)", cpu['brand']],
                    ["Hardware", "Architecture", cpu['architecture']],
                    ["Hardware", "Physical Cores", f"{cpu['cores_physical']} cores"],
                    ["Hardware", "Logical Cores", f"{cpu['cores_logical']} cores"],
                    ["Hardware", "CPU Frequency", f"{cpu['frequency_ghz']} GHz" if cpu['frequency_ghz'] != "Unknown" else "Unknown"],
                    ["Hardware", "Graphics (GPU)", self.system_info['gpu']],
                    ["Hardware", "Total RAM", f"{memory['total_gb']} GB"],
                    ["Hardware", "Available RAM", f"{memory['available_gb']} GB"],
                    ["Hardware", "Memory Type", memory['type']],
                    ["Hardware", "Storage Total", f"{storage['total_gb']} GB"],
                    ["Hardware", "Storage Available", f"{storage['free_gb']} GB"],
                    ["Hardware", "Storage Type", storage['type']],
                    ["Hardware", "Network Interfaces", self.system_info['network']]
                ]
                
                # Software section
                os_info = self.system_info['os']
                packages = self.system_info['packages']
                
                software_rows = [
                    ["Software", "Operating System", f"{os_info['name']} {os_info['release']}"],
                    ["Software", "OS Platform", os_info['platform']],
                    ["Software", "Python Version", os_info['python_version']],
                    ["Software", "Charm-Crypto", packages.get('charm-crypto', 'Not installed')],
                    ["Software", "Cryptography", packages.get('cryptography', 'Not installed')],
                    ["Software", "PyCryptodome", packages.get('pycryptodome', 'Not installed')],
                    ["Software", "Web3.py", packages.get('web3', 'Not installed')],
                    ["Software", "IPFS HTTP Client", packages.get('ipfshttpclient', 'Not installed')],
                    ["Software", "NumPy", packages.get('numpy', 'Not installed')],
                    ["Software", "Pandas", packages.get('pandas', 'Not installed')]
                ]

                # Blockchain tools section
                blockchain_tools = self.system_info['blockchain_tools']
                blockchain_rows = [
                    ["Blockchain/IPFS", "IPFS", blockchain_tools.get('IPFS', 'Not installed')],
                    ["Blockchain/IPFS", "Ganache CLI", blockchain_tools.get('Ganache CLI', 'Not installed')],
                    ["Blockchain/IPFS", "Truffle", blockchain_tools.get('Truffle', 'Not installed')],
                    ["Blockchain/IPFS", "Go Ethereum", blockchain_tools.get('Go Ethereum (geth)', 'Not installed')]
                ]
                
                # Write all rows
                writer.writerows(hardware_rows + software_rows + blockchain_rows)
                
                # Add metadata
                writer.writerow([])
                writer.writerow(["Metadata", "Collection Time", self.system_info['collection_time']])
            
            print(f"\nConfiguration exported to: {csv_path}")
            
        except Exception as e:
            print(f"Error exporting to CSV: {str(e)}")

    def generate_latex_table(self):
        """Generate LaTeX table format for academic papers"""
        print("\n" + "="*80)
        print("LATEX TABLE FORMAT (for Section 6.1 - Academic Paper)")
        print("="*80)
        
        latex_code = """
% Hardware and Software Configuration Table for ABE Performance Study
% Insert this in Section 6.1 (Page 25) as requested by Reviewer 1
\\begin{table}[htbp]
\\centering
\\caption{Experimental Environment Configuration}
\\label{tab:experimental_config}
\\begin{tabular}{|l|l|}
\\hline
\\textbf{Component} & \\textbf{Specification} \\\\
\\hline
\\multicolumn{2}{|c|}{\\textbf{Hardware Configuration}} \\\\
\\hline
"""
        
        # Add hardware info
        cpu = self.system_info['cpu']
        memory = self.system_info['memory']
        storage = self.system_info['storage']
        
        # Escape special LaTeX characters and format for academic standards
        cpu_brand = cpu['brand'].replace('&', '\\&').replace('_', '\\_')
        latex_code += f"Processor & {cpu_brand} \\\\\n"
        latex_code += f"Architecture & {cpu['architecture']} \\\\\n"
        latex_code += f"Physical/Logical Cores & {cpu['cores_physical']}/{cpu['cores_logical']} \\\\\n"
        if cpu['frequency_ghz'] != "Unknown":
            latex_code += f"CPU Frequency & {cpu['frequency_ghz']} GHz \\\\\n"
        
        gpu_info = self.system_info['gpu'].replace('&', '\\&').replace('_', '\\_')
        latex_code += f"Graphics Processing Unit & {gpu_info} \\\\\n"
        latex_code += f"System Memory & {memory['total_gb']} GB {memory['type']} \\\\\n"
        latex_code += f"Storage & {storage['total_gb']} GB {storage['type']} \\\\\n"
        latex_code += "\\hline\n"
        latex_code += "\\multicolumn{2}{|c|}{\\textbf{Software Environment}} \\\\\n"
        latex_code += "\\hline\n"
        
        # Add software info
        os_info = self.system_info['os']
        packages = self.system_info['packages']
        
        os_name = f"{os_info['name']} {os_info['release']}".replace('_', '\\_')
        latex_code += f"Operating System & {os_name} \\\\\n"
        latex_code += f"Python Runtime & {os_info['python_version']} \\\\\n"
        latex_code += f"Charm-Crypto Library & {packages.get('charm-crypto', 'N/A')} \\\\\n"
        latex_code += f"Cryptography Library & {packages.get('cryptography', 'N/A')} \\\\\n"
        latex_code += f"Web3 Library & {packages.get('web3', 'N/A')} \\\\\n"
        latex_code += "\\hline\n"
        latex_code += "\\multicolumn{2}{|c|}{\\textbf{Blockchain \\& IPFS Tools}} \\\\\n"
        latex_code += "\\hline\n"
        
        # Add blockchain tools
        blockchain_tools = self.system_info['blockchain_tools']
        latex_code += f"IPFS & {blockchain_tools.get('IPFS', 'N/A')} \\\\\n"
        latex_code += f"Ganache CLI & {blockchain_tools.get('Ganache CLI', 'N/A')} \\\\\n"
        latex_code += f"Truffle Framework & {blockchain_tools.get('Truffle', 'N/A')} \\\\\n"
        
        latex_code += """\\hline
\\end{tabular}
\\end{table}

% Usage Note: 
% This table provides comprehensive hardware and software configuration details
% as requested by Reviewer 1 for inclusion in Section 6.1 (page 25).
% The configuration ensures reproducibility of ABE performance experiments.
"""
        
        print(latex_code)
        
        # Save to file
        latex_file = "/Users/thanhtuan/son/ABE/samples/system_config_table.tex"
        try:
            with open(latex_file, 'w', encoding='utf-8') as f:
                f.write(latex_code)
            print(f"LaTeX table saved to: {latex_file}")
        except Exception as e:
            print(f"Error saving LaTeX file: {str(e)}")


def main():
    """Main function to run system information collection"""
    print("System Information Collection for ABE Performance Study")
    print("=" * 60)
    print("Comprehensive hardware/software configuration for Reviewer 1 requirements")
    print("=" * 60)
    
    collector = SystemInfoCollector()
    
    # Generate and display academic table
    collector.generate_academic_table()
    
    # Export to CSV
    collector.export_to_csv()
    
    # Generate LaTeX format
    collector.generate_latex_table()
    
    print("\n" + "="*80)
    print("REVIEWER 1 RESPONSE - CONFIGURATION TABLE:")
    print("="*80)
    print("✓ Hardware details: CPU, RAM, Storage, GPU")
    print("✓ Software environment: OS, Python, Crypto libraries") 
    print("✓ Blockchain/IPFS versions: IPFS, Ganache, Truffle")
    print("✓ LaTeX format ready for Section 6.1 (page 25)")
    print("✓ CSV export for data analysis")
    print("✓ Comprehensive specification for experiment reproducibility")
    print("="*80)


if __name__ == "__main__":
    main()
