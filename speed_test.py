import requests
import sys
import itertools
import threading
import time
from termcolor import colored

def api_req():
  try:
    req = requests.get('https://quote-garden.herokuapp.com/api/v3/quotes/random') #random quote request
    json = req.json()
    quote = json['data']
    return quote[0]['quoteText']
  except requests.ConnectionError:
    sys.exit()


def main():
  done = False
  def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
      if done:
          break
      sys.stdout.write('\rloading request ' + c)
      sys.stdout.flush()
      time.sleep(0.1)

  t = threading.Thread(target=animate)
  t.start()
  time.sleep(3)
  done = True

  prompt = api_req()
  print('\n\n<<', colored(prompt, 'yellow'), '\n')

  while True: 
    timerStart = time.perf_counter()
    write = input('>> ')
    timerStop = time.perf_counter()

    prompt_l = prompt.strip().split(" ")
    write_l = write.strip().split(" ")

    if len(prompt_l) == len(write_l):
      break
    else:
      print(colored(f'missed {len(prompt_l) - len(write_l)} words', 'red'), 'retry writing the sentence completely\n')

  count = 0
  err_list = []    
  for i in range(len(prompt_l)):
    if prompt_l[i].lower() != write_l[i].lower():
      count += 1
      err_list.append(write_l[i])

  wps = len(write) / 60
  err_rate = ((len(prompt_l) - (len(prompt_l) - count)) / len(prompt)) * 100
  acc = 100 - err_rate
  print()
  if count == 0:
    print(f'you did {colored(f"{count} mistakes", "green")} done')
  else:  
    print(colored(f"{count} mistakes", "red"), 'done')        

  if (timerStop - timerStart) < 60:
    timer = timerStop - timerStart
    print('it took you ', colored(f'{round(timer, 2)} seconds', 'yellow'))
  else:
    timer =  (timerStop - timerStart) * 0.016666666666667
    print('it took you ', colored(f'{round(timer, 2)} minutes', 'yellow'))

  print(f'typing speed of {colored(f"{round(wps, 3)} wps", "magenta")} (words per seconds)')
  print(f'with {colored("accuracy", "yellow")} of', colored(f'{round(acc, 2)}%', 'yellow'))

  if count != 0:
    while True:
      err_print = input('\nprint mistakes? (y/[n]) -> ')
      if err_print == 'y' or err_print == 'Y':
        for i in range(len(err_list)):
          print(colored(err_list[i], 'red'))
        print()
        break
      else:
        break

try:
  main()
except KeyboardInterrupt:
  print(colored('shutting all down!', 'red'))