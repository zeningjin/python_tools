#coding=utf-8

import pandas as pd

def write_json_to_xls(datas, file_name):
    df = pd.DataFrame(datas)
    df.to_excel(r'%s.xlsx' % file_name)
    # df.to_excel(file_name)

if __name__ == '__main__':
    data = {0: {'update_flow_datas_by_bill_type': 0.059945106506347656, 'get_flow_datas_and_create_xlsx_by_pipe_ids': 11.058834075927734, 'get_bill_type_by_pipe_id': 0.22885704040527344, 'All time spend': 21.945388078689575, 'new_download_graph': 10.59775185585022}, 1: {'update_flow_datas_by_bill_type': 0.0662698745727539, 'get_flow_datas_and_create_xlsx_by_pipe_ids': 11.520264148712158, 'get_bill_type_by_pipe_id': 0.19154882431030273, 'All time spend': 24.567484855651855, 'new_download_graph': 12.78940200805664}, 2: {'update_flow_datas_by_bill_type': 0.06560516357421875, 'get_flow_datas_and_create_xlsx_by_pipe_ids': 11.782668828964233, 'get_bill_type_by_pipe_id': 0.20378708839416504, 'All time spend': 23.587816953659058, 'new_download_graph': 11.53575587272644}, 3: {'update_flow_datas_by_bill_type': 0.07160592079162598, 'get_flow_datas_and_create_xlsx_by_pipe_ids': 11.668183088302612, 'get_bill_type_by_pipe_id': 0.19167590141296387, 'All time spend': 23.65854001045227, 'new_download_graph': 11.727075099945068}, 4: {'update_flow_datas_by_bill_type': 0.06781506538391113, 'get_flow_datas_and_create_xlsx_by_pipe_ids': 11.535928010940552, 'get_bill_type_by_pipe_id': 0.199476957321167, 'All time spend': 24.204759120941162, 'new_download_graph': 12.401539087295532}, 5: {'update_flow_datas_by_bill_type': 0.07114291191101074, 'get_flow_datas_and_create_xlsx_by_pipe_ids': 12.0624361038208, 'get_bill_type_by_pipe_id': 0.21532392501831055, 'All time spend': 23.781600952148438, 'new_download_graph': 11.432698011398315}, 6: {'update_flow_datas_by_bill_type': 0.06174921989440918, 'get_flow_datas_and_create_xlsx_by_pipe_ids': 10.823952913284302, 'get_bill_type_by_pipe_id': 0.17818593978881836, 'All time spend': 22.01621103286743, 'new_download_graph': 10.952322959899902}, 7: {'update_flow_datas_by_bill_type': 0.05899405479431152, 'get_flow_datas_and_create_xlsx_by_pipe_ids': 11.178443908691406, 'get_bill_type_by_pipe_id': 0.17416810989379883, 'All time spend': 21.99246597290039, 'new_download_graph': 10.580859899520874}, 8: {'update_flow_datas_by_bill_type': 0.06950688362121582, 'get_flow_datas_and_create_xlsx_by_pipe_ids': 11.001094102859497, 'get_bill_type_by_pipe_id': 0.1764819622039795, 'All time spend': 22.14269995689392, 'new_download_graph': 10.895617008209229}, 9: {'update_flow_datas_by_bill_type': 0.060281991958618164, 'get_flow_datas_and_create_xlsx_by_pipe_ids': 11.450947046279907, 'get_bill_type_by_pipe_id': 0.18558907508850098, 'All time spend': 22.313003063201904, 'new_download_graph': 10.616184949874878}}
    file_name = '批量导出监控数据-测试'
    write_json_to_xls(data, file_name)
