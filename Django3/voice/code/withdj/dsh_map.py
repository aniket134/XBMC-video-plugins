import logging,dsh_utils

callers = {
    '09935237793': ['DSH', 'Randy Wang'],
    '09795190920': ['DSH', 'Sumeet Khullar'],
    '09621559142': ['DSH', 'Sumeet Khullar'],
    '09839014341': ['DSH', 'Urvashi Sahni'],
    '09984491377': ['DSH', 'Richaa Himanshu'],
    '09936349668': ['Sewa', 'Pratima Shrivastava'],
    '09918550289': ['Sewa', 'Zunaira Ansari'],
    '09305244032': ['Sewa', 'Shazia Khan'],
    '09415768870': ['Sewa', 'Nazia Ansari'],
    '09889365300': ['Sewa', 'Ghazala'],
    '09450638919': ['Sewa', 'Preeti'],
    '09307173448': ['Sewa', 'Shagufta Praveen'],
    '09935690187': ['Prerna', 'Roli'],
    '09453302888': ['Prerna', 'Bharti Bhatia'],
    '09794226470': ['Prerna', 'Vandana Singh'],
    '09335823710': ['Prerna', 'Indu Bhatia'],
    '09450654825': ['Prerna', 'Rakhi Panjwani'],
    '09616605010': ['EduAcad', 'Jyoti Kumari'],
    '09335900175': ['EduAcad', 'Praveen Shukla'],
    '09307828696': ['EduAcad', 'Parul Yadav'],
    '09935555676': ['EduAcad', 'Bijendra Kumar'],
    '09005754703': ['Mauthri', 'Kanta Sharma'],
    '09956399360': ['Mauthri', 'Krishna Sharma'],
    '09369897445': ['Mavaiya', 'Vishun'],
    '09935483950': ['Mavaiya', 'Sushma'],
    '09305890156': ['Springdale', 'Ranjana'],
    '09307051179': ['Springdale', 'Anita Singh'],
    '09307168021': ['Springdale', 'Khushboo'],
    '09307874578': ['Springdale', 'Sheeba'],
    '09794632188': ['Springdale', 'Ashish Singh'],
    '09322101109': ['Springdale', 'Sonia'],
    '09305187234': ['Springdale', 'Sonia'],
    '09451077945': ['Madantoosi', 'Siya Ram'],
    '09793082974': ['Madantoosi', 'Mohan Rawat'],
    '09838773439': ['Madantoosi', 'Sharda Singh'],
    '09793084594': ['Madantoosi', 'Ravindra Singh'],
    '09415959464': ['Madantoosi', 'R Yadav'],
    '09792436224': ['Vidyasthali', 'Samuel Singh'],
    '09369239766': ['Vidyasthali', 'Kalpana Tripathi'],
    '09839770479': ['Vidyasthali', 'Priya Seth'],
    '09984440090': ['Vidyasthali', 'Suruchi Saraswat'],
    '09305512750': ['Vidyasthali', 'Deepti Tandon'],
    '09336604375': ['Vidyasthali', 'Pradeep Shukla'],
    '09198891053': ['Vidyasthali', 'Sanjay Verma'],
    '09454615782': ['Vidyasthali', 'Kanchan'],
    '09305457800': ['Vidyasthali', 'Renu Gupta'],
    '09305894199': ['Vidyasthali', 'Anupama Dube'],
    '09936349668': ['Vidyasthali', 'Pratima Srivastava'],
    '09936198624': ['Vidyasthali', 'Vineeta Yadav'],
    '09005206115': ['Vidyasthali', 'Dr Pratima'],
    '09455617241': ['Gangaganj', 'Umesh Chandra'],
    '09935175302': ['Gangaganj', 'R Singh'],
    '09307625897': ['Gangaganj', 'Umesh Chaudhary'],
    '09208056821': ['Gangaganj', 'Sushil Verma'],
    '09415085070': ['Gangaganj', 'Ram Singh'],
    '09919670380': ['Gangaganj', 'Hariom Mishra'],
    '09918065793': ['Gangaganj', 'Shiv Shankar'],
    '09450065869': ['Gangaganj', 'Avnish Kumar'],
    'unknown': ['mystery place', 'no name']
}



def lookup(phoneNumber):
    if callers.has_key(phoneNumber):
        return callers[phoneNumber]
    return callers['unknown']



def log_caller_info(phoneNumber, callerInfo):
    school,name = callerInfo
    logStr = '|| ' + phoneNumber + ' || ' + school + ' || ' + name + ' || '
    dsh_utils.give_news('dsh_map.log_caller_info: ' + logStr, logging.info)
    return logStr



def info2str(phoneNumber, callerInfo):
    return dsh_utils.strip_join_str(phoneNumber + '_' +
                                    callerInfo[0] + '_' + callerInfo[1])
