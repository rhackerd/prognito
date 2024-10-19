import os
import questionary
import shutil
import argparse

class ProjectGenerator:
    def __init__(self, templates_dir, project_dir):
        self.project_name = ""
        self.srcfolder = "src"
        self.mainfile = "main.cpp"
        self.templates_dir = templates_dir
        self.project_dir = project_dir

    def list_templates(self):
        """List available templates in the templates directory."""
        templates = [
            d for d in os.listdir(self.templates_dir) 
            if os.path.isdir(os.path.join(self.templates_dir, d))
        ]
        return templates

    def create_build_script(self):
        return f"""#!/bin/bash

# Define variables
srcfolder="{self.srcfolder}"
mainfile="{self.mainfile}"
output="main"

# Compile the C++ source file
gcc -o ${{srcfolder}}/$output ${{srcfolder}}/$mainfile

# Run the compiled program (optional)
# ./${{srcfolder}}/$output
"""

    def create_cmake_file(self, libraries):
        cmake_content = """cmake_minimum_required(VERSION 3.10)
project(MyProject)

set(CMAKE_CXX_STANDARD 14)

add_executable(main src/main.cpp)
"""
        if libraries:
            cmake_content += "target_link_libraries(main " + " ".join(libraries) + ")\n"

        return cmake_content

    def generate_project(self):
        self.project_name = questionary.text("Enter project name:").ask()
        
        # Create project directory
        project_path = os.path.join(self.project_dir, self.project_name)
        os.makedirs(project_path, exist_ok=True)

        # List templates and ask for user choice
        if os.path.exists(self.templates_dir):
            templates = self.list_templates()
            if templates:
                chosen_template = questionary.select(
                    "Choose a template:",
                    choices=templates
                ).ask()
                template_src = os.path.join(self.templates_dir, chosen_template, self.mainfile)
                if os.path.exists(template_src):
                    # Create source directory
                    os.makedirs(os.path.join(project_path, self.srcfolder), exist_ok=True)
                    # Copy template main.cpp to the new project
                    shutil.copy(template_src, os.path.join(project_path, self.srcfolder, self.mainfile))
                else:
                    print(f"No main.cpp found in template '{chosen_template}'.")
                    return
            else:
                print("No templates found.")
                return
        else:
            print(f"Templates directory '{self.templates_dir}' does not exist.")
            return

        # Create build.sh
        with open(os.path.join(project_path, "build.sh"), "w") as f:
            f.write(self.create_build_script())

        # Ask about CMake
        if questionary.confirm("Do you want to add CMake support?").ask():
            # Ask for libraries
            libraries = questionary.text("Enter libraries to link (space-separated):").ask()
            libraries_list = libraries.split() if libraries else []
            with open(os.path.join(project_path, "CMakeLists.txt"), "w") as f:
                f.write(self.create_cmake_file(libraries_list))

        # Make build.sh executable
        os.chmod(os.path.join(project_path, "build.sh"), 0o755)

        print(f"Project '{self.project_name}' created successfully.")

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Generate a C++ project.")
    parser.add_argument("-t", "--templates", type=str, 
                        default=os.path.expanduser("~/Dokumenty/prognito/templates/"), 
                        help="Path to the templates directory.")
    parser.add_argument("-d", "--dir", type=str, 
                        default=os.getcwd(), 
                        help="Directory to create the project.")
    
    args = parser.parse_args()

    # Create the ProjectGenerator instance with specified directories
    generator = ProjectGenerator(args.templates, args.dir)
    generator.generate_project()

if __name__ == "__main__":
    main()
