import email
import csv
import os

emails = os.listdir("GDPR_opt_ins")
csv_columns = ["Title", "First Name", "Last Name", "Email", "Option_Phone", "Option_Email", "Option_SMS",
               "Option_Post_Mag", "Option_Email_Mag", "Option_Newsletter", "Option_Challenges"]
details_list = []
completed_count = 0
failed_count = 0
post_count = 0
duplicate_count = 0


def extract_info(email_content):
    # get email contents line by line
    content_lines = email_content.split("\n")
    details_dict = {}
    check_fields = 0
    # Check each line for certain tags and extract data if tag found.
    for index, line in enumerate(content_lines):
        if '<ul class="bulleted">' in line:
            # If post is selected skip email due to inconsistencies in address input.
            if "Post" in content_lines[index + 1]:
                file.close()
                global post_count
                post_count += 1
                return False
            if "Email" in content_lines[index + 1]:
                details_dict["Option_Email"] = "Yes"
            if "SMS" in content_lines[index + 1]:
                details_dict["Option_SMS"] = "Yes"
            if "Phone" in content_lines[index + 1]:
                details_dict["Option_Phone"] = "Yes"
            if "Helimed Magazine (posted twice a year)" in content_lines[index + 1]:
                details_dict["Option_Post_Mag"] = "Yes"
            if "Helimed Magazine (emailed twice a year)" in content_lines[index + 1]:
                details_dict["Option_Email_Mag"] = "Yes"
            if "Email newsletter (once a month)" in content_lines[index + 1]:
                details_dict["Option_Newsletter"] = "Yes"
            if "Our Challenges (via email)" in content_lines[index + 1]:
                details_dict["Option_Challenges"] = "Yes"
        if "Title" in line:
            title = remove_html(content_lines[index + 5])
            details_dict["Title"] = title
            check_fields += 1
        if "First Name" in line:
            first_name = remove_html(content_lines[index + 5])
            details_dict["First Name"] = first_name
            check_fields += 1
        if "Last Name" in line:
            last_name = remove_html(content_lines[index + 5])
            details_dict["Last Name"] = last_name
            check_fields += 1
        if "Please enter your email address" in line:
            email_add = remove_html(content_lines[index + 5])
            details_dict["Email"] = email_add

    # check if title, first and last name are present, add to dictionary and delete email if true.
    if check_fields == 3:
        if details_dict not in details_list:
            details_list.append(details_dict)
            global completed_count
            completed_count += 1
        else:
            # If any duplicates for all fields do not add to csv file and delete email.
            global duplicate_count
            duplicate_count += 1
        file.close()
        os.remove(location)

    else:
        # If the extraction fails add to the failed count and return without deleting the email
        global failed_count
        failed_count += 1
        return False


def remove_html(text):
    # Remove and html data from around the extracted text to leave the required data
    new_text = text.replace('<td><font style="font-family: sans-serif; font-size:12px;">', "")
    new_text = new_text.replace('</td>', "")
    new_text = new_text.replace("</font>", "")
    new_text = new_text.replace("<li>", "")
    new_text = new_text.replace("</li></ul>", "")
    return new_text


# read each file in specified email folder and if it is an email read the email data and call the extract_info function
for mail in emails:
    if ".msg" in mail:
        location = os.path.join("GDPR_opt_ins", mail)
        file = open(location, "r", errors="ignore")
        email_content = email.message_from_file(file)
        extract_info(str(email_content))

# create or open csv file and add a new line for each record
with open("GDPR_opt_ins.csv", "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for detail in details_list:
        writer.writerow(detail)

# Print summary of emails to console once complete and wait for user to confirm by pressing enter key
print(f"Number of completed emails: {completed_count}")
print(f"Number of duplicates ignored: {duplicate_count}")
print(f"Number of failed emails: {failed_count}")
print(f"Number of emails with post selected for manual entry: {post_count}")
input("Press enter key to finish")
