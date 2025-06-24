from setuptools import setup, find_packages

setup(
    name='mini_siri_assistant',
    version='0.0.1',
    author='DhananiPavan',
    author_email='dhananipavan369@gmail.com',
    install_requires=[
        "speechrecognition",
        "pyttsx3",
        "pywhatkit",
        "openai",
        "python-dotenv",
        "pyaudio"
    ],
    packages=find_packages()
)
# This setup script is used to package the mini_siri_assistant project.