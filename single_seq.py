__author__ = 'Tierprot'

from selenium import webdriver
import os
import time

# TODO : Use expectedConditions instead of wait directive.
# TODO : Sometimes Jpred spits out proxy error, next time it will
# TODO : spit it, don`t forget to wrap that case into try/except

class single_query():
    # finished job archive will be downloaded into this directory
    download_dir = os.path.join(os.getcwd(), 'download')    

    # main input area default tag
    seq_tab_tag = 'textarea'

    # advanced options tags/names/xpath`s default values
    advanced_options_id = 'showMore'
    pdb_xpath = "//*[@name='pdb']"
    email_name = 'email'
    job_name = 'queryName'
    submit_xpath = "//*[@type='submit']"
    result_archive = 'Get all files in TAR.GZ archive'
    in_queque = 'chklog?keywords='

    def __init__(self, url='http://www.compbio.dundee.ac.uk/jpred/'):
        # instantiating custom profile
        self.browser = webdriver.Firefox(self.profile())
        try:
            self.browser.get(url)
        except Exception as Exp:
            print(Exp)

    # preconfigured FireFox profile
    def profile(self):
        if os.path.exists(self.download_dir):
            pass
        else:
            os.mkdir(self.download_dir)

        FirefoxProfile = webdriver.FirefoxProfile()
        FirefoxProfile.set_preference('browser.download.folderList', 2)
        FirefoxProfile.set_preference('browser.download.manager.showWhenStarting', False)
        FirefoxProfile.set_preference('browser.download.dir', self.download_dir)
        FirefoxProfile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/x-gzip')
        return FirefoxProfile

    # <======Query config===========>
    # paste sequence into form
    def paste_query(self, seq, seq_tab_tag=seq_tab_tag):
        try:
            self.browser.find_element_by_tag_name(seq_tab_tag).clear()
            self.browser.find_element_by_tag_name(seq_tab_tag).send_keys(seq)
        except Exception:
            print("Warning, query wasn`t pasted!")

    # open advanced options
    def open_advanced_options(self, advanced_options_id=advanced_options_id):
        try:
            self.browser.find_element_by_id(advanced_options_id).click()
            time.sleep(1)
        except Exception:
            print("Warning, advanced options button wasn`t found!")

    # check that PDB search is turned off
    def check_PDB(self, xpath=pdb_xpath):
        try:
            self.browser.find_element_by_xpath(xpath).click()
        except Exception:
            print("Warning, PDB radio button wasn`t found!")

    # paste email if it was provided
    def provide_email(self, email, email_name=email_name):
        try:
            self.browser.find_element_by_name(email_name).send_keys(email)
        except Exception:
            print("Warning, email field wasn`t found!")

    # paste job title
    def provide_job_title(self, title, job_name=job_name):
        try:
            self.browser.find_element_by_name(job_name).send_keys(title)
        except Exception:
            print("Warning, job title field wasn`t found!")

    # submit data to server
    def submit(self, submit_xpath=submit_xpath):
        try:
            self.browser.find_element_by_xpath(submit_xpath).click()
        except Exception:
            print("Warning, submit button wasn`t found!")

    def download_results(self, result_archive=result_archive, in_queque=in_queque):
        try:
            self.browser.find_element_by_link_text(result_archive).click()
            print("Job is ready!")

            # check wheter donwload is complete
            filename = self.browser.find_element_by_link_text(result_archive).get_attribute('href')
            filename = filename.split('/')[-1]
            print(filename)

            while(True):
                time.sleep(3)

                #if original file and .part are existing or at least .part exists - continue
                if os.path.exists(os.path.join(self.download_dir, filename)) & \
                        os.path.exists(os.path.join(self.download_dir, filename+'.part')) or\
                    os.path.exists(os.path.join(self.download_dir, filename+'.part')):
                    continue
                else:
                    break

            self.browser.quit()

            return True

        except Exception:
            print("Not ready yet")
            try:
                self.browser.find_element_by_partial_link_text(in_queque).click()
                print("Job in a process of submission, but server doesn`t know about it yet")
            except Exception:
                pass