import requests
from bs4 import BeautifulSoup

# کدهای ANSI برای رنگ‌ها
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"

def check_domain_status(domain):
    url = f"https://whois.nic.ir/WHOIS?name={domain}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"خطا در ارتباط با سرور whois.nic.ir برای دامنه '{domain}'"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    answer_section = soup.find('pre')
    
    if answer_section:
        answer_text = answer_section.get_text()
        if "ERROR:101" in answer_text:
            return f"{COLOR_GREEN}دامنه '{domain}' ثبت نشده است و می‌توانید آن را ثبت کنید.{COLOR_RESET}"
        elif "domain:" in answer_text:
            return f"{COLOR_RED}دامنه '{domain}' ثبت شده است.{COLOR_RESET}\n{answer_text}"
    
    return f"وضعیت دامنه '{domain}' مشخص نیست."

def read_domains_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            domains = [line.strip() for line in file if line.strip()]
        return domains
    except FileNotFoundError:
        print(f"فایل '{file_path}' یافت نشد.")
        return []

def main():
    file_path = "domains.txt"  # مسیر فایل حاوی دامنه‌ها
    domains = read_domains_from_file(file_path)
    
    if not domains:
        print("هیچ دامنه‌ای در فایل یافت نشد.")
        return
    
    for domain in domains:
        # domain_with_ir = domain + ".ir"  # اضافه کردن پسوند .ir
        domain_with_ir = domain 
        result = check_domain_status(domain_with_ir)
        print(result)
        print("-" * 50)  # جداکننده برای خوانایی بیشتر

if __name__ == "__main__":
    main()