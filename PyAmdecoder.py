from binascii import hexlify
import sys

string_list=[]

def lb(test):
    return int.from_bytes(test, byteorder='little')

def check_routine(data,prefix,uri,xmlns_count,tab):
    routine_type=lb(data[:2])
    if(routine_type==0x100):
        XML_START_NAMESPACE(data,tab)
    elif(routine_type==0x101):
        XML_END_NAMESPACE(data,tab)
    elif(routine_type==0x102):
        XML_START_ELEMENT(data,prefix,uri,xmlns_count,tab)
    elif(routine_type==0x103):
        XML_END_ELEMENT(data,prefix,uri,xmlns_count,tab)
        
def XML_END_ELEMENT(data,prefix,uri,xmlns_count,tab):
    end_ELEMENT_type=lb(data[:2])
    end_ELEMENT_header_size=lb(data[2:4])
    end_ELEMENT_chunk_size=lb(data[4:8])
    end_ELEMENT_line_number=lb(data[8:12])
    end_ELEMENT_comment=lb(data[12:16])
    end_ELEMENT_ns=lb(data[16:20])
    end_ELEMENT_name=lb(data[20:24])
    print(tab*"\t"+"</"+string_list[end_ELEMENT_name]+">")
    tab-=1
    return check_routine(data[24:],prefix,uri,xmlns_count,tab)
    
def XML_END_NAMESPACE(data,tab):
    end_namespace_type=lb(data[:2])
    end_namespace_header_size=lb(data[2:4])
    end_namespace_chunk_size=lb(data[4:8])
    end_namespace_line_number=lb(data[8:12])
    end_namespace_comment=lb(data[12:16])
    end_namespace_prefix=lb(data[16:20])
    end_namespace_uri=lb(data[20:24])
    tab-=1
    return check_routine(data[24:],end_namespace_prefix,end_namespace_uri,1,tab)
    
def XML_START_ELEMENT(data,prefix,uri,xmlns_count,tab):
    tab+=1
    element_type=lb(data[:2])
    element_header_size=lb(data[2:4])
    element_chunk_size=lb(data[4:8])
    element_line_number=lb(data[8:12])
    element_comment=lb(data[12:16])
    element_ns=lb(data[16:20])
    element_name=lb(data[20:24])
    element_attribute_start=lb(data[24:26])
    element_attribute_size=lb(data[26:28])
    element_attribute_count=lb(data[28:30])
    element_id_index=lb(data[30:32])
    element_class_index=lb(data[32:34])
    element_style_index=lb(data[34:36])
    if(xmlns_count==0):
        print(tab*"\t"+"<"+string_list[element_name],"\n"+tab*"\t"+"\txmlns:"+prefix+"=\""+uri+"\"")
    else:
        print(tab*"\t"+"<"+string_list[element_name])
        
    data=data[36:]
    for i in range(element_attribute_count):
        attribute_ns=lb(data[:4])
        attribute_name=lb(data[4:8])
        attribute_raw_value=lb(data[8:12])
        attribute_size=lb(data[12:14])
        attribute_0=lb(data[14:15])
        attribute_dataType=lb(data[15:16])
        attribute_data=lb(data[16:20])
        if(attribute_dataType==0x03):
            temp_val=string_list[attribute_data]
        elif(attribute_dataType==0x01):
            temp_val="@"+str(hex(attribute_data))[2:]
        elif(attribute_dataType==0x12):
            if attribute_data==0:
                temp_val="false"
            else:
                temp_val="true"
        elif(attribute_dataType==0x11):
            temp_val=str(hex(attribute_data))
        else:
            temp_val=str(attribute_data)
            
        if(attribute_ns!=0xffffffff):
            print(tab*"\t"+"\t"+prefix+":"+string_list[attribute_name]+"=\""+str(temp_val)+"\"")
        else:
            print(tab*"\t"+"\t"+string_list[attribute_name]+"=\""+str(temp_val)+"\"")
        data=data[20:]
    print(tab*"\t"+"\t>")
    if(data):
        check_routine(data,prefix,uri,1,tab)
        
    
def XML_START_NAMESPACE(data,tab):
    namespace_type=lb(data[:2])
    namespace_header_size=lb(data[2:4])
    namespace_chunk_size=lb(data[4:8])
    namespace_line_number=lb(data[8:12])
    namespace_comment=lb(data[12:16])
    namespace_prefix=lb(data[16:20])
    namespace_uri=lb(data[20:24])
    tab+=1
    XML_START_ELEMENT(data[24:],string_list[namespace_prefix],string_list[namespace_uri],0,tab)
    
def Resource_Map(data):
    Resource_Type=lb(data[0:2])
    Resource_header_size=lb(data[2:4])
    Resource_Chunk_size=lb(data[4:8])
    XML_START_NAMESPACE(data[Resource_Chunk_size:],-2)
    
def Make_String_List(data,count):
    for i in range(count):
        String_len=lb(data[:2])
        string_bin=data[2:String_len*2+4]
        string_list.append(string_bin.decode('utf-16')[:-1])
        data=data[String_len*2+4:]
    if(lb(data[:2])==0):
        Resource_Map(data[2:])
    else:
        Resource_Map(data)
    
    
def String_Pool(data):
    String_Pool_Type=lb(data[0:2])
    String_Pool_Header_Size=lb(data[2:4])
    String_Pool_Chunk_Size=lb(data[4:8])
    String_Pool_String_Count=lb(data[8:12])
    String_Pool_Style_Count=lb(data[12:16])
    String_Pool_flags=lb(data[16:20])
    String_Pool_StringStart=lb(data[20:24])
    String_Pool_StyleStart=lb(data[24:28])
    Make_String_List(data[String_Pool_StringStart:],String_Pool_String_Count)

 
def PyAmdecoder(file_name):
    sys.setrecursionlimit(10000)
    f=open(file_name,"rb")
    fdata = f.read()
    f.close()
    print('<?xml version="1.0" encoding="utf-8"?>')
    XML_type=lb(fdata[0:2])
    XML_Header_Size=lb(fdata[2:4])
    XML_Chunk_Size=lb(fdata[4:8])
    String_Pool(fdata[XML_Header_Size:])
