import pandas as pd
import datetime
import pdfkit as pdf

# make ontext manager 
class File(object):
	
    def __init__(self, filename, mode):
        self.filename = filename 
        self.mode = mode 
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    def __exit__(self, exec_type, exec_val, traceback):
        self.file.close()

class FileUpdateSystem(File):
    
    def __init__(self, *a ,**kw):
        self.a = a 
        self.kw = kw

    def convert_data_to_html_table(self):
        pass
    
    # make sure to copy the line as its represented
    def deleteLine(self, filename, lines_to_delete):
        # filtering 
        for line_to_delete in lines_to_delete:
            with File(filename, 'r+') as f:
                output = []
                content = f.readlines()
                for line in content:
                    if line.startswith(line_to_delete):
                        print('deleted line: ',line)
                        pass
                    else:
                        output.append(line)
        # rewriting 
        with File(filename, 'w') as f:
            for line in output:
                f.write(line)
    
    def series_to_list(self, series):
        list_ = [i for i in series]
        return list_

    def generate_table(
        self, 
        reference_number=False, 
        main=False, 
        additional_tasks=False, 
        signature=False, 
        date_taken=False, 
        revision_date=False
    ):  

        if main:
            significant_hazards = input('significant_hazards:')
            potential_consequences_of_hazard = input('potential_consequences_of_hazard:')
            initial_risk_level = input('initial_risk_level:')
            existing_control_measures = input('existing_control_measures:')
            additional_control_measures = input('additional_control_measures:')
            final_risk_level = input('final_risk_level:')
            overall_risk = input('overall_risk:')

            if overall_risk == 'Low':
                color = 'green'
            elif overall_risk == 'Medium':
                color = 'yellow'
            elif overall_risk == 'High':
                color = 'orange'
            else:
                color = 'Red'
            print(color)
            
            
            #Date = datetime.datetime.now()
            #Revision_date = input()

            table_of_contents = f'''
                        <tr>
                            <td>{significant_hazards}</td>
                            <td>{potential_consequences_of_hazard}</td>
                            <td>{initial_risk_level}</td>
                            <td>{existing_control_measures}</td>
                            <td>{additional_control_measures}</td>
                            <td>{final_risk_level}</td>
                        </tr>
                    '''
        elif reference_number:
            
            reference_n = input('your_reference_number:')
            table_of_contents = f'''
                        <th>{reference_n}</th>
            '''
        elif additional_tasks:

            addit_tasks = input('additional_tasks_and_references:')
            table_of_contents = f'''
                        <th>{addit_tasks}</th>
            '''
        elif signature:

            author = input('author_name:')
            table_of_contents = f'''
                        <th>{author}</th>
            '''
        
        elif date_taken:

            date_carried_out = input('date_risk_assessment_was_carried_out:')
            table_of_contents = f'''
                        <th>{date_carried_out}</th>
            ''' 
        elif revision_date:
    
            date_revisited = input('date_risk_assessment_was_revised:')
            table_of_contents = f'''
                        <th>{date_revisited}</th>
            '''

        else:      
            table_of_contents = 'none'


        with File('info.html', 'w') as f:
            f.write(table_of_contents)

    def copy_into_ra(self, filename, section_to_target, secondary_step=False):

        with File(filename, 'r') as fin, File('output.html', 'w') as fout, File('info.html', 'r') as content:
            table = content.read()
            fin_list = fin.readlines()
            for line in fin_list:
                
                fout.write(line)
                if line == section_to_target + '\n':
                    fout.write(table)
                    fout.write('\n')
                else:
                    pass
        filename = filename if secondary_step else 'output.html'

        with File(filename, 'w') as fout, File('output.html', 'r') as fin:
            content = fin.read()
            fout.write(content)


reference_number_indicator = '                        <th><strong>Reference number</strong></th>.'
main_indicators = '                    </tr>.'
date_indicator = '                        <th><strong>Date:</strong></th>.'
revision_date_indicator = '                        <th><strong>Revision Date:</strong></th>.'
signature_indicator = '                        <th><strong>Undertaken by:</strong></th>.'
additional_tasks_indicator = '                        <th><strong>Additional References and Tasks:</strong></th>.'

fus = FileUpdateSystem()

fus.generate_table(reference_number=True)
fus.copy_into_ra('risk_assessment.html',reference_number_indicator)

fus.generate_table(main=True)
fus.copy_into_ra('risk_assessment.html',main_indicators, secondary_step=True)

fus.generate_table(additional_tasks=True)
fus.copy_into_ra('risk_assessment.html',additional_tasks_indicator, secondary_step=True)

fus.generate_table(signature=True)
fus.copy_into_ra('risk_assessment.html',signature_indicator, secondary_step=True)

fus.generate_table(date_taken=True)
fus.copy_into_ra('risk_assessment.html',date_indicator, secondary_step=True)

fus.generate_table(revision_date=True)
fus.copy_into_ra('risk_assessment.html',revision_date_indicator, secondary_step=True)


#to download the file download the wkhtmltox.exe file from https://wkhtmltopdf.org/downloads.html
#then run the following code
#pdf.from_file('risk_assessment.html', 'risk_assessment.pdf')