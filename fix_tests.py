import os
import glob

directory = r'f:\Labibaupdate1fullcopy\InfraSyncBD\InfraSyncBD\selenium_tests'
for filename in glob.glob(os.path.join(directory, '*.py')):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    new_content = []
    lines = content.split('\n')
    for line in lines:
        if 'driver.find_element(By.XPATH, "//button[@type=\'submit\']").click()' in line:
            indentation = line[:len(line) - len(line.lstrip())]
            new_content.append(indentation + 'login_btn = driver.find_element(By.XPATH, "//button[@type=\'submit\']")')
            new_content.append(indentation + 'driver.execute_script("arguments[0].click();", login_btn)')
        else:
            new_content.append(line)
            
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('\n'.join(new_content))
    print(f'Updated {filename}')
