def unicode_safe_print(string_to_print):
  try:
    print(string_to_print)
  except UnicodeEncodeError:
    # print char by char, replacing non-printable characters by ?
    for ch in string_to_print:
      try:
        print(ch, end="")
      except UnicodeEncodeError:
        print('?', end="")
    print("")