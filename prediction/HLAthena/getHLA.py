import csv
import os
import re
import time
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

SITE_URL = 'http://hlathena.tools/'
DRIVER_PATH = os.path.join(os.getcwd(), 'driver', 'geckodriver')
INPUT_PATH = sys.argv[1]
OUT_PATH = os.path.join(os.getcwd(), 'output')

# all th HLA type can be queryed via hlathena
HLA_LIST = [
    'A0101', 'A0201', 'A0202', 'A0203', 'A0204', 'A0205', 'A0206', 'A0207', 'A0211', 'A0301', 'A1101', 'A1102', 'A2301', 
    'A2402', 'A2407', 'A2501', 'A2601', 'A2902', 'A3001', 'A3002', 'A3101', 'A3201', 'A3301', 'A3303', 'A3401', 'A3402', 
    'A3601', 'A6601', 'A6801', 'A6802', 'A7401', 'B0702', 'B0704', 'B0801', 'B1301', 'B1302', 'B1402', 'B1501', 'B1502', 
    'B1503', 'B1510', 'B1517', 'B1801', 'B2705', 'B3501', 'B3503', 'B3507', 'B3701', 'B3801', 'B3802', 'B4001', 'B4002',
    'B4006', 'B4201', 'B4402', 'B4403', 'B4501', 'B4601', 'B4901', 'B5001', 'B5101', 'B5201', 'B5301', 'B5401', 'B5501', 
    'B5502', 'B5601', 'B5701', 'B5703', 'B5801', 'B5802', 'C0102', 'C0202', 'C0302', 'C0303', 'C0304', 'C0401', 'C0403', 
    'C0501', 'C0602', 'C0701', 'C0702', 'C0704', 'C0801', 'C0802', 'C1202', 'C1203', 'C1402', 'C1403', 'C1502', 'C1601', 
    'C1701', 'G0101', 'G0103', 'G0104'
]
PAGE_LOAD_TIMEOUT = 10
FILE_UPLOAD_TIMEOUT = 60


def switch_tab_to_predict(browser):
    browser.refresh()
    # change tab pane
    tab = WebDriverWait(browser, PAGE_LOAD_TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.navbar-nav>li:nth-child(3)')))
    assert tab.text == 'Predict'
    tab.click()


def download_is_completed(out_dir):
    for i in os.listdir(os.path.join(os.getcwd(), out_dir)):
        # firefox download file 'example.txt' as 0 byte 'example.txt' and a downloading file 'example.txt.part'
        # if there's no '.part' file in downloading dir, download is completed
        if '.part' in i:
            return False
    return True


def get_single_output(browser, HLA, peptide, timeout=360):
    switch_tab_to_predict(browser)
    # set form values
    browser.execute_script(f"$('#allele_pred').selectize()[0].selectize.setValue(['{HLA}'])")
    seq_input = browser.find_element_by_id('peptide_pred')
    seq_input.clear()
    seq_input.send_keys(peptide)
    # wait for ws tunnel updating(~0.1s), wait 1s for secure
    time.sleep(1)
    submit_button = browser.find_element_by_id('predict_button')
    submit_button.click()
    # wait result
    output = WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.ID, 'predict_peptide')))
    return output.text


def get_multi_output(browser, HLA, seq_file, timeout=720):
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            switch_tab_to_predict(browser)
            time.sleep(1)
            # set form values
            browser.execute_script(f"$('#allele_pred').selectize()[0].selectize.setValue(['{HLA}'])")
            dir_path = os.path.dirname(os.path.abspath(__file__))
            abs_seq_file_path = os.path.join(dir_path, seq_file)
            file_input = browser.find_element_by_id('peptide_pred_file').send_keys(abs_seq_file_path)
            # wait for completion of file uploading
            WebDriverWait(browser, FILE_UPLOAD_TIMEOUT).until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'progress-bar'), 'Upload complete'))
            # check whether col_index is 'pep'
            peptide_col_index = browser.find_element_by_id('peptide_col_name')
            assert peptide_col_index.get_attribute('value') == 'pep'
            time.sleep(1)
            submit_button = browser.find_element_by_id('predict_button')
            submit_button.click()
            # wait result
            download_button = WebDriverWait(browser, timeout).until(EC.element_to_be_clickable((By.ID, 'downloadPredictions')))
            # wait for js and socket updating(append href to download action link)
            WebDriverWait(browser, PAGE_LOAD_TIMEOUT).until(lambda dr: 'downloadPredictions' in dr.find_element_by_id('downloadPredictions').get_attribute('href'))
            download_url = browser.find_element_by_id('downloadPredictions').get_attribute('href')
            browser.execute_script(f"window.open('{download_url}')")
            success = True
        except TimeoutException:
            print(f"{HLA}: trying again...")
            attempts += 1
            if attempts == 3:
                print(f"'{HLA}': '{seq_file}' Timeout Error!")


def get_result_from_single_seq(browser, seq_file, res_file='output.txt'):
    with open(seq_file) as input_file, open(res_file, 'w') as output_file:
        reader = csv.reader(input_file)
        for row in reader:
            HLA_record, peptide = row[0:2]
            HLA = re.sub(r'HLA-(.{1})\*(\d{2}):(\d{2})', r'\g<1>\g<2>\g<3>', HLA_record)
            out = get_single_output(browser, HLA, peptide) if HLA in HLA_LIST else 'Can\'t search'
            output_file.write(f"{HLA}\t{peptide}\n{out}\n\n\n")


def get_result_from_multi_seq(browser, seq_file, hla_list):
    # get a predict tsv-file for each hla type
    for HLA in hla_list:
        get_multi_output(browser, HLA, seq_file)
        print(f"{HLA} prediction done!")



def main():
    start = 1
    end = len(os.listdir(os.path.join(os.getcwd(), INPUT_PATH)))
    if sys.argv[2:4]:
        start, end = sys.argv[2:4]

    data_source_list = [ f"cos_pep_{i}" for i in range(int(start), int(end) + 1) ]

    for data_source in data_source_list:
        print(f'Task {data_source} Start')
        
        download_dir = os.path.join(OUT_PATH, data_source)
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)

        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showhenStarting", False)
        fp.set_preference("browser.download.dir", download_dir)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/tab-separated-values")

        opt = webdriver.FirefoxOptions()
        opt.add_argument('-headless')

        browser = webdriver.Firefox(executable_path=DRIVER_PATH, firefox_profile=fp, options=opt)
        browser.get(SITE_URL)

        get_result_from_multi_seq(browser, seq_file=f'input/{data_source}.txt', hla_list=HLA_LIST)

        time.sleep(20)
        while not download_is_completed(download_dir):
            time.sleep(5)
            print('waiting for downloading...')
        
        browser.quit()
        print('Task Complete')
    


if __name__ == "__main__":
    if sys.version_info < (3, 7):
        print('Python version over 3.7 is required!')
        raise(EnvironmentError)

    main()
    print('All Task Complete!')
