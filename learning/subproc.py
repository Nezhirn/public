import subprocess

def bash_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
        #print(f"Результат выполнения команды:\n{result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Ошибка выполнения команды:")
        print(e.stderr)
        return None

command = 'curl https://chatgpt.com/' # Исправленная команда

result = bash_command(command)
print(result)
