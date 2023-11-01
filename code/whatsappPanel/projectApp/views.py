
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from django.shortcuts import render
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException
from django.http import HttpResponse
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging
import pandas as pd
from django.core.files.storage import default_storage
import os
from openpyxl import Workbook
import xlsxwriter
from django.http import JsonResponses
from django.shortcuts import redirect
from django.urls import  reverse
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from django.conf import settings




def base(request):
        return render(request, 'index.html')

def tour_page(request):
    return render(request, 'base.html')




'''def upload(request):
    if request.method == 'POST' or request.method == 'GET':
        xlsx_file = request.FILES.get('xlsxFile')
        img_file = request.FILES.get('imgFile')
        message = request.POST.get('message', '')

        is_excel_valid = xlsx_file is not None
        is_image_valid = img_file is not None and img_file.content_type.startswith('image')
        is_message_valid = message.strip() != ''

        if not is_excel_valid or not is_image_valid or not is_message_valid:
            return HttpResponse("Please upload an XLSX file, an image, and a message.")
        elif is_image_valid and is_excel_valid and is_message_valid:
            return redirect('whatsapp_automation_img_and_message')

        # Handle other cases or invalid form data
        return HttpResponse('Invalid form data.')

    return HttpResponse('Invalid request method.')'''

'''def is_image_valid(request):
    # Your logic for image validation
    if request.FILES.get('imgFile'):
        # Your validation logic here
        return True
    return False

def is_excel_valid(request):
    # Your logic for Excel file validation
    if request.FILES.get('xlsxFile'):
        # Your validation logic here
        return True
    return False

def is_message_valid(request):
    # Your logic for message validation
    if request.POST.get('message'):
        # Your validation logic here
        return True
    return False'''


import json
from django.http import JsonResponse



def whatsapp_automation(request):
    if request.method == 'POST':
        xlsx_file = request.FILES['xlsxFile'] if 'xlsxFile' in request.FILES else None
        message = request.POST.get('message', '')
        print(message, xlsx_file)
        if not xlsx_file:
            return JsonResponse({'error': "No file uploaded."})

        invalid_numbers = []
        numbers = []

        try:
            data = pd.read_excel(xlsx_file)
            data.columns = data.columns.str.strip()  # Trim column names
            if 'mobile' in data.columns:
                numbers = data['mobile'].tolist()  # Adjust as per your column name
            else:
                raise KeyError("Column 'mobile' not found in the Excel file.")
        except KeyError as e:
            return JsonResponse({'error': f"Failed to read the file. Error: {e}"})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read the file. Error: {e}"})

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        link = 'https://web.whatsapp.com'
        driver.get(link)

        time.sleep(20)  # You may need to adjust the sleep time

        for num in numbers:
            try:
                send_url = f'https://web.whatsapp.com/send?phone=+91{num}&text={message}'
                driver.get(send_url)
                try:
                    invalid_number_pop_up = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@role="alert"]')))
                    invalid_number_pop_up.find_element(By.XPATH, '//span[contains(text(), "OK")]').click()
                    print(f"Invalid number: {num}")
                    invalid_numbers.append(num)
                except:
                    try:
                        '''link = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
                        action = ActionChains(driver)
                        action.send_keys(Keys.ENTER)
                        action.perform()
                        print(f"Message sent to: {num}")'''
                        send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]')))
                        send_button.click()
                        try:
                           image_sent = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "image-thumb")]')))
                           print(f"Image uploaded successfully for: {num}")
                        except Exception as e:
                           print(f"Image upload unsuccessful for: {num}. Error: {e}")
                    except Exception as e:
                        print(f"Failed to send message to: {num}. Error: {e}")
            except Exception as e:
                print(f"Failed to send message to: {num}. Error: {e}")

            time.sleep(10)

        driver.quit()

        if len(invalid_numbers) == 0:
            return JsonResponse({'status': "WhatsApp messages sent successfully"})
        else:
            return JsonResponse({'error': f"Failed to send messages to numbers: {invalid_numbers}"})
    else:
        return JsonResponse({'error': "Please use a valid request method (POST)."})



#code for sending image

'''def whatsapp_automation_img(request):
    print(f"Request method: {request.method}")  
    if request.method == 'POST':
        xlsx_file = request.FILES['xlsxFile'] if 'xlsxFile' in request.FILES else None# Adjust as per your form field names
        img_file = request.FILES.get('imgFile')  if 'imgFile' in request.FILES else None # Adjust as per your form field names
        #message = request.POST.get('message')  
        #print(message)# Set up loggingif not xlsx_file:
        if not xlsx_file:
            return JsonResponse({'error': "No file uploaded."})

        invalid_numbers = []
        numbers = []

        try:
            data = pd.read_excel(xlsx_file)
            data.columns = data.columns.str.strip()  # Trim column names
            if 'mobile' in data.columns:
                numbers = data['mobile'].tolist()  # Adjust as per your column name
            else:
                raise KeyError("Column 'mobile' not found in the Excel file.")
        except KeyError as e:
            return JsonResponse({'error': f"Failed to read the file. Error: {e}"})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read the file. Error: {e}"})

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        link = 'https://web.whatsapp.com'
        driver.get(link)

        time.sleep(20)  # You may need to adjust the sleep time

          # Adjust the sleep time as needed

        for num in numbers:
          try:
             send_url = f'https://web.whatsapp.com/send?phone=+91{num}'
             driver.get(send_url)
             time.sleep(20)
             try:
                # Wait for the invalid number pop-up to appear
                invalid_number_pop_up = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH, '//div[@role="alert"]')))
                # Click the "OK" button to dismiss the pop-up
                invalid_number_pop_up.find_element(By.XPATH, '//span[contains(text(), "OK")]').click()
                print(f"Invalid number: { invalid_numbers}")
             except:
                try:
                      attachment_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[title="Attach"]')))
                      attachment_button.click()
                      time.sleep(2)

                      image_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
                      image_path = img_file
                      image_button.send_keys(image_path)
                      time.sleep(2)

                      # Send the image
                      send_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-icon="send"]')))
                      send_button.click()

                except NoSuchElementException as e:
                    logging.error(f"Error occurred: {e}")
                    continue

          except Exception as e:
                        print(f"Failed to send message to: {numbers}. Error: {e}")
        time.sleep(20)  # Adjust the sleep time as needed

    driver.quit()
        
    if len(invalid_numbers) == 0:
            return JsonResponse({'status': "WhatsApp messages sent successfully"})
    else:
            return JsonResponse({'error': f"Failed to send messages to numbers: {invalid_numbers}"})
   
    return JsonResponse({'error': "Please use a valid request method (POST)."})'''




# ... (other imports)
def save_uploaded_file_locally(uploaded_file):
    
    if uploaded_file:
        file_extension = uploaded_file.name.split('.')[-1]
        file_path = f'path_to_store_image.{file_extension}'
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        return os.path.abspath(file_path)
    else:
        return None
    


def whatsapp_automation_img(request):
    print(f"Request method: {request.method}")
    if request.method == 'POST':
        xlsx_file = request.FILES['xlsxFile'] if 'xlsxFile' in request.FILES else None
        img_file = request.FILES['imgFile'] if 'imgFile' in request.FILES else None
        image_path = save_uploaded_file_locally(img_file)


        if not xlsx_file or not img_file:
            return JsonResponse({'error': "No file uploaded."})

        invalid_numbers = []
        numbers = []

        try:
            data = pd.read_excel(xlsx_file)
            data.columns = data.columns.str.strip()
            if 'mobile' in data.columns:
                numbers = data['mobile'].tolist()
            else:
                raise KeyError("Column 'mobile' not found in the Excel file.")
        except KeyError as e:
            return JsonResponse({'error': f"Failed to read the file. Error: {e}"})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read the file. Error: {e}"})

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        link = 'https://web.whatsapp.com'
        driver.get(link)

        time.sleep(20)

        for num in numbers:
            try:
                send_url = f'https://web.whatsapp.com/send?phone=+91{num}'
                driver.get(send_url)
                time.sleep(20)
                try:
                    invalid_number_pop_up = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH, '//div[@role="alert"]')))
                    invalid_number_pop_up.find_element(By.XPATH, '//span[contains(text(), "OK")]').click()
                    invalid_numbers.append(num)
                    print(f"Invalid number: {num}")
                except:
                        attachment_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@title="Attach"]')))
                        attachment_button.click()
                        time.sleep(2)

                        image_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
                        image_button.send_keys(image_path) 
                        time.sleep(5) # Pass the file name or path here
                        #send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="send"]')))
                        send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]')))
                        send_button.click()
                        try:
                           image_sent = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "image-thumb")]')))
                           print(f"Image uploaded successfully for: {num}")
                        except Exception as e:
                           print(f"Image upload unsuccessful for: {num}. Error: {e}")
    # Add this number to the list of invalid numbers
                           invalid_numbers.append(num)

            except Exception as e:
                print(f"Failed to send message to: {num}. Error: {e}")
                invalid_numbers.append(num)

        time.sleep(20)
        driver.quit()

        if len(invalid_numbers) == 0:
            return JsonResponse({'status': "WhatsApp messages sent successfully"})
        else:
            return JsonResponse({'error': f"Failed to send messages to numbers: {invalid_numbers}"})

    return JsonResponse({'error': "Please use a valid request method (POST)."})








# Other imports...

def whatsapp_automation_img_and_message(request):
    if request.method == 'POST':
        xlsx_file = request.FILES['xlsxFile'] if 'xlsxFile' in request.FILES else None
        img_file = request.FILES['imgFile'] if 'imgFile' in request.FILES else None
        image_path = save_uploaded_file_locally(img_file)# Adjust as per your form field names
        message = request.POST.get('message','')

        if not xlsx_file:
            return JsonResponse({'error': "No file uploaded."})

        invalid_numbers = []
        numbers = []

        try:
            data = pd.read_excel(xlsx_file)
            data.columns = data.columns.str.strip()  # Trim column names
            if 'mobile' in data.columns:
                numbers = data['mobile'].tolist()  # Adjust as per your column name
            else:
                raise KeyError("Column 'mobile' not found in the Excel file.")
        except KeyError as e:
            return JsonResponse({'error': f"Failed to read the file. Error: {e}"})
        except Exception as e:
            return JsonResponse({'error': f"Failed to read the file. Error: {e}"})

        driver = webdriver.Chrome(ChromeDriverManager().install())
        link = 'https://web.whatsapp.com'
        driver.get(link)
        time.sleep(20)

        for num in numbers:
            try:
                send_url = f'https://web.whatsapp.com/send?phone=+91{num}'
                driver.get(send_url)
                print(send_url)
                try:
                    invalid_number_pop_up = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@role="alert"]')))
                    invalid_number_pop_up.find_element(By.XPATH, '//span[contains(text(), "OK")]').click()
                    invalid_numbers.append(num)
                    print(invalid_numbers)
                except TimeoutException:
                    print(f"No alert found for the number {num}. Moving to the next number.")
                    
                    try:
                        attachment_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@title="Attach"]')))
                        attachment_button.click()
                        time.sleep(8)

                        image_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
                        image_button.send_keys(image_path) 
                        time.sleep(8)

                        input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]')))
                        message = message
                        input_field.send_keys(message)
                        time.sleep(2)
                        send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]')))
                        send_button.click()
                        try:
                           image_sent = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "image-thumb")]')))
                           print(f"Image and message uploaded successfully for: {num}")
                        except Exception as e:
                           print(f"Image upload unsuccessful for: {num}. Error: {e}")
    # Add this number to the list of invalid numbers
                        

                        #send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]')))
                        #send_button.click()
                    except:
                        print(f"Failed to send message to: {numbers}. Error: {e}")
            except:
                print(f"Failed to send message to: {num}. ")

            time.sleep(10)

        driver.quit()
        if len(invalid_numbers) == 0:
            return JsonResponse({'status': 'success', 'message': 'WhatsApp images and messages sent successfully'})
        else:
            return JsonResponse({'error': 'Failed to send any images or messages.'})
    else:
        return JsonResponse({'error': 'Please use a valid request method (POST).'})









