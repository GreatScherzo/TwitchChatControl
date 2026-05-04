import win32gui

def find_window_by_title(title_substring):
    hwnd = win32gui.FindWindow(None, title_substring)
    return hwnd

def win_enum_handler(hwnd, ctx):
    if win32gui.IsWindowVisible( hwnd ):
        print (hex(hwnd), win32gui.GetWindowText( hwnd ))

def win_enum_handler_list(hwnd, passed_list:list):
    # The handler will parse through each window, it seems
    # list will be passed via extra_param variable
    window_title = win32gui.GetWindowText(hwnd)

    if win32gui.IsWindowVisible( hwnd ):
        window_title = window_title
        # print (hex(hwnd), win32gui.GetWindowText( hwnd ))
        if passed_list is not None:
            passed_list.append({"hwnd": hwnd, "title": window_title})

def search_window_with_name(search_string: str, list):
    for curr_dict in list:
        title_str: str = curr_dict['title']
        if search_string in title_str:
            return curr_dict['hwnd']


if __name__ == '__main__':
    # Example: Find a window with "Notepad" in its title
    window_handle = find_window_by_title("VisualBoyAdvance-M 2.1.11")

    # test = win32gui.EnumWindows(winEnumHandler, None)
    window_list = []
    win32gui.EnumWindows(win_enum_handler_list, window_list)
    true_window_handle = search_window_with_name("VisualBoyAdvance-M 2.1.11", window_list)
    if true_window_handle:
        win32gui.SetForegroundWindow(true_window_handle)
    else:
        print("Window not found.")