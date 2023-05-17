from f247_crawler import _run_247
from f319_crawler import _run_319
from viettrader import _run_viettrader

if __name__ == '__main__':
    while True:
        search_kw = str(input("Nhập keyword: "))
        forum_selection = input("Chọn forum (319: f319.com    -     247: f247.com    -   100: traderviet.net) : ")
        if forum_selection == "319":
            _run_319(search_kw)
        elif forum_selection == "247":
            _run_247(search_kw)
        elif forum_selection == "100":
            _run_viettrader(search_kw)
        print("--------------------- finished ----------------------")
        is_exit = input("Nhấn 0 để kết thúc, nhấn 1 để tiếp tục...  ")
        if is_exit == '0':
            break
        elif is_exit == '1':
            continue
