import re
n = 0
f1 = open('ah_data_2.txt','w+')
with open('ah_data2.txt') as f:
    line = f.readline()
    while line:
        #每一行做匹配和替换
        
        #报账单号
        #_report_number_====================TYA01211140500021709013005
        #_report_number_====================TYB01211170100021709019008 
        #_report_number_====================JKA01211190002011709000001
        #_report_number_====================RGA01211130000111710001004  
        
        #串码531004990070344000000495739FC31E 1B1004990070344000000495739FB04A
        serial_code= re.compile(r"[a-zA-Z0-9]{32}")
        line = serial_code.sub('_serial_',line)
        
        #地区编码
        #area_code
        area_code= re.compile(r"【[0-9]{7}】")
        line = area_code.sub('_area_',line)
        #因为很长，所以不会有误差
        report_number = re.compile(r"[a-zA-Z]{3}[0-9]{23}")
        line = report_number.sub('_report_',line)
        
        #运维单号
        #Operation_maintenance ==========CO2017092255018301556 
        Operation_maintenance = re.compile(r"CO[0-9]{19}")
        line = Operation_maintenance.sub('_operate_',line)
        
        #工单号 
        #_list_number_==========TZ00002017092920544387
        #_list_number_==========EG2017101955318353643
        #_list_number_==========EG201701455118346144
        list_number = re.compile(r"[a-zA-Z]{2}00002017[0-9]{12}|EG2017[0-9]{15}|EG2017[0-9]{14}")
        line = list_number.sub('_list_',line)
#         list_number1 = re.compile(r"工单号[0-9]{7,}")
        #前面包含工单号
        list_number1 = re.compile(r"(?<=工单号)[0-9]{7,}")
        line = list_number1.sub('_list_',line)

        
        #流水号 
        #_flowing_number_ =============1000000200201709301550561487     
        #_flowing_number_ =============15201710040048875767 
        #_flowing_number_ =============04170925556321097878   
        #_flowing_number_ =============JTSH201700034215
        flowing_number = re.compile(r"10000002002017[0-9]{14}")
        line = flowing_number.sub('_flow_',line)
        flowing_number1 = re.compile(r"152017[0-9]{14}")
        line = flowing_number1.sub('_flow_',line)
        flowing_number2 = re.compile(r"JTSH2017[0-9]{8}")
        line = flowing_number2.sub('_flow_',line)
        flowing_number3 = re.compile(r"[0-9]{20}")
        line = flowing_number3.sub('_flow_',line)
        
        
        #ITV 账号    13 12 11位
        #_ITV_=================IPTV5512013325960
        #_ITV_=================IPTV55120161184635 
        #_ITV_=================IPTV550201277902
        ITV = re.compile(r"IPTV5[0-9]{13}|IPTV5[0-9]{12}|IPTV5[0-9]{11}")
        line = ITV.sub('_ITV_',line)        
                
        #宽带Broadband===============KDYX55620162266165
        #宽带Broadband===============ADS5632010344232
        #宽带Broadband===============ADS556200527338
        #宽带Broadband===============ADS5534873 ADS5534873
        Broadband = re.compile(r"KDYX[0-9]{14}|ADS[0-9]{13}|ADS[0-9]{12}|ADS[0-9]{7}|adsl[0-9]{10}")
        line = Broadband.sub('_NET_',line)

        #证号
        #_certificate_number_=========[342301701110083:15375608075]
        certificate_number = re.compile(r"[0-9]{8,}:[0-9]{8,}")
        line = certificate_number.sub('_certify_',line)
        
        #IP
        IP = re.compile(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,}\.[0-9]{1,3}|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,}\,[0-9]{1,3}")
        line = IP.sub('_IP_',line)
        
        
        #工程编号
        #_project_number_ ============17AH006802001  16AH013792001 17HA013594001 17AH007350 161AAHTL0211 7AH002644001
        project_number = re.compile(r"[0-9]{2}AH[0-9]{9}|[0-9]{2}HA[0-9]{9}|[0-9]{2}AH[0-9]{6}|[0-9]HA[0-9]{9}")
        line = project_number.sub('_project_',line)
     
        
        #采购订单编号
        #_purchase_order_number_===========================AHDD201704110233 
        #_purchase_order_number_===========================AHDD201602030032
        purchase_order_number = re.compile(r"AHDD201[0-9]{9}")
        line = purchase_order_number.sub('_purchase_',line)
        
        #集团支付号码
        #_group_payment_number_======JTZF551139173  JTZF562114833
        group_payment_number = re.compile(r"JTZF[0-9]{9}")
        line = group_payment_number.sub('_pay_',line)
        
        #串号
        #_serial_number_============A000007283EE81   A100005C471BC5 
        #这个应该是少写了一位0==========A0000688F2284
        serial_number = re.compile(r"A[0-1]{1}0000[0-9\a-zA-Z]{8}")
        line = serial_number.sub('_serial_num_',line)
        serial_number1 = re.compile(r"A[0-1]{1}000[0-9\a-zA-Z]{8}")
        line = serial_number1.sub('_serial_num_',line)
        
        
        #工单
        #work_order ==================YJXQ2017100155618311427
        work_order = re.compile(r"YJXQ2017[0-9]{15}")
        line = work_order.sub('_work_',line)
        
        #业务号
        #_business_number_==============HLWZX559201738704 
        business_number = re.compile(r"HLWZX[0-9]{12}")
        line = business_number.sub('_business_',line)
        
        #单据ID
        #_document_ID_====================110000221757364 
        #_document_ID_====================ZC112017929002384
        document_ID = re.compile(r"110000[0-9]{9}|ZC\d{15}")
        line = document_ID.sub('_document_',line)
        
        #电话号码
#         phone_number = re.compile(r"号码：[0-9]{7}|号码[0-9]{7}|[0-9]{7}[号]")
#         line = phone_number.sub('_phone_number_',line)

        
        #卡号
        #card_number
        card_number = re.compile(r"(?<!【)[0-9]{19}")
        line = card_number.sub('_card_',line)
        
        #身份证号
        #ID_number
        ID_number = re.compile(r"(?<!【)[0-9]{17}[0-9]|[0-9]{17}X")
        line = ID_number.sub('_ID_',line)
        
        
        #合同号
        #contract_number=====================AHSGG1601216CGN00 
        #contract_number=====================AHXCG1500064AGN00
        #contract_number=====================100042737586 这个应该是输入错误，不管
        #contract_number=====================1000157615329
        #contract_number=====================Ng109339 只出现一次，不管
        #contract_number=====================S000395  也是少数，且标明了合同号，不管
        #contract_number=====================J5286 只出现一次，不管

        contract_number = re.compile(r"[a-zA-Z]{5}[0-9]{7}[a-zA-Z]{3}[0-9]{2}")
        line = contract_number.sub('_contract_',line)
        contract_number1 = re.compile(r"1000[0-9]{9}|1000[0-9]{8}|Ng[0-9]{6}")
        line = contract_number1.sub('_contract_',line)

        
        #客户编码
        #_customer_code_=============255201517295 256005631597 
        customer_code = re.findall(r"25[0-9]{10,}",line)
        for customer_codes in customer_code:
            if len(customer_codes)==12:
                line= line.replace(customer_codes,"_customer_")
                print(line)        
        
        #手机号
        phone1 = re.findall(r"1\d{10,}",line)  
        for phone1s in phone1:
#             print(phone1s)
            if len(phone1s)==11:
#                 print(phone1s)
                line= line.replace(phone1s,"_phone_")
#                 print(line)

        #电路
        #_electric_
        electric = re.compile(r"CIR\d{5,}")
        line= electric.sub('_electric_',line)
        
        #时间
        #time ================= 201709 2017-09-22
        time = re.compile(r"20[0,1][0-9]\-[0-1][0-9]\-[0-3][0-9]")
        line= time.sub('_time_',line)
        time = re.findall(r"20[0,1][0-9][0-3][0-9]{1,}",line)
        for times in time:
            if len(times) == 6:
                line = line.replace(times,"_time_")
        #20[0,1][0-9][0-3][0-9]|
        #工号
        #job_number==============H8159137 55109800
        job_number = re.findall(r"[A-Z]\d{7,}",line)
        for job_numbers in job_number:
            if len(job_numbers)==8:
                line= line.replace(job_numbers,"_job_")
        

        
        #订单号
        #order_number============128165725 255585613
        #先取出这一行的数字
        order_number = re.findall(r"(?<!【)[0-9]{9,}",line)
        for order_numbers in order_number:
            if len(order_numbers)==9:
                line= line.replace(order_numbers,"_order_")
#         order_number = re.compile(r"[订单号：]\d{6,}")
#         line= order_number.sub('_order_number_',line)
        
        #工号
        job_number1 = re.findall(r"\d{8,}",line)
        for job_number1s in job_number1:
            if len(job_number1s)==8:
                line= line.replace(job_number1s,"_job_")
                
                
        #工号：860201
        job_number = re.compile(r"(?<=工号)\d{5,}")
        line= job_number.sub('_job_',line)
        #只匹配一次的做法
#         job_number = re.compile(r"[A-Z]\d{7,}")
#         matcher1 = re.search(job_number,line)
#         if matcher1:
#             length = len(matcher1[0])
#             if length == 8:
#                 line = job_number.sub('_job_number_',line)
        
#         phone_number = re.compile(r"[0-9]{7}|")
#         line = phone_number.sub('_phone_number_',line)
        #密码
        #password
        password = re.compile(r"hqs\d{7}")
        line= password.sub('_pass_',line)
        #核对金额
        amount = re.compile(r"\-\d{7}")
        line= amount.sub('_amount_',line)
        
        phone_number = re.findall(r"\d{7,}",line)
        for phone_numbers in phone_number:
            if len(phone_numbers)==7:
                line= line.replace(phone_numbers,"_tel_")  

        print(line)
        f1.writelines(line)
        line = f.readline()
        



