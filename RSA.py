#Importowanie bibliotek
import time
import os
from random import randint

try: #kolory
    from colorama import init, Fore
    init()
except:
    print("Cannot import colorama!")

try: #cuda
    import cupy as cp
    use_cuda = True
except:
    print(Fore.RED + "!!!Cannot import CUPY, using CPU mode!!!", Fore.RESET)
    use_cuda = False

def Beep(duration = 0.40):
    try:
        import winsound
        frequency = 800
        Duration = int(1000 * duration)
        winsound.Beep(frequency, Duration)
    except:
        print("")

######################   KLASY   #####################
class Szyfrowanie():
    def __init__(self,filepath = "",e = -1, d = -1, n = -1):
        start = time.perf_counter()

        #zbiór liczb pierwszych
        if (use_cuda):
            self.pierwsze = cp.array([101,
            103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,
            199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,
            313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,
            433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,
            563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,
            673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,
            811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,
            941,947,953,967,971,977,983,991,997])
        else:
            self.pierwsze = [101,
            103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,
            199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,
            313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,
            433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,
            563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,
            673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,
            811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,
            941,947,953,967,971,977,983,991,997]

        #zmienne do szyfrowania plików
        self.p = 1
        self.q = 1
        self.N = 1

        self.e = 1
        self.d = 1

        self.euler = 1

        if ((e <= 0 or d <= 0 or n <= 0) and (filepath == None or filepath == "")):
            #generowanie kluczy
            self.generate_keys()
        else:
            print(Fore.GREEN + "Ustawiam klucze: " + Fore.RESET)
            
            if (filepath == "" or filepath == None):
                self.e = e
                self.d = d
                self.N = n
            else:
                self.read_keys(filepath)
            print("e =",self.e)
            print("d =",self.d)
            print("N =",self.N)


        #time
        duration = time.perf_counter() - start
        print(Fore.GREEN + "\nZakończono w" + Fore.RESET + " [ ",end="")
        if (duration < 60):
            print(duration,"s ]")
        else:
            minuty = int(duration / 60)
            sekundy = duration % 60
            print(minuty,"min,",sekundy,"sec ]")
        print("\n")

    def generate_keys(self):
        print(Fore.GREEN + "\nGeneruję p",Fore.RESET)
        self.p = self.pierwsze[randint(0,self.pierwsze.size-1)]
        print("p =",self.p)

        print(Fore.GREEN + "Generuję q",Fore.RESET)
        self.q = self.pierwsze[randint(0,self.pierwsze.size-1)]
        print("q =",self.q)

        self.N = self.p * self.q


        print(Fore.GREEN + "Obliczam funkcję eulera" + Fore.RESET + " dla",self.N)
        self.euler = (self.q-1)*(self.p-1)
        print("O(N) =",self.euler)

        #klucze
        self.find_e()
        self.find_d()

        print(Fore.LIGHTRED_EX + "\nKlucz publiczny:",Fore.RESET , "(" , self.e , "," , self.N , ")")
        print(Fore.LIGHTRED_EX + "Klucz prywatny:",Fore.RESET , "(" , self.d , "," , self.N , ")")

    def find_e(self):
        helper1 = 0
        helper2 = 0
        e1 = e2 = 1

        print(Fore.GREEN + "Szukam e",Fore.RESET)

        while(True):
            self.e += 1
            e1 = self.e
            e2 = self.e
            helper1 = self.N
            helper2 = self.euler

            while(e1 != helper2):
                if (e1 > helper2):
                    e1 = e1 - helper2
                else:
                    helper2 = helper2 - e1

            while(helper1 != e2):
                if (helper1 > e2):
                    helper1 = helper1 - e2
                else:
                    e2 = e2 - helper1
            
            if ((e2 == 1) and (e1 == 1)):
                break

        print("e =",self.e)

    def find_d(self):
        print(Fore.GREEN + "Szukam d",Fore.RESET)
        while(True):
            self.d += 1
            if ((self.e * self.d) % self.euler == 1):
                break
        print("d =", self.d)

    def save_key(self,filepath:str):
        print(Fore.CYAN + "Zapisuję klucz publiczny",Fore.RESET)
        try:
            path = filepath + "-public.txt"
            f = open(path,"w+")
            key = str(self.e) + "\n" + str(self.N)
            f.write(key)
            f.close()
            print(Fore.GREEN + "Zapisano" + Fore.RESET)
        except Exception as e:
            print(Fore.RED + "Zapis nieudany\n", Fore.RESET , e)

        print(Fore.CYAN + "Zapisuję klucz prywatny",Fore.RESET)
        try:
            path = filepath + "-private.txt"
            f = open(path,"w+")
            key = str(self.d) + "\n" + str(self.N)
            f.write(key)
            f.close()
            print(Fore.GREEN + "Zapisano" + Fore.RESET)
        except Exception as e:
            print(Fore.RED + "Zapis nieudany\n", Fore.RESET , e)

    def read_keys(self,filepath:str):
        print(Fore.CYAN + "Wczytuję klucze z plików" + Fore.RESET)
        self.d = 1
        self.e = 1
        self.N = 1
        try:
            path = filepath + "-public.txt"
            f = open(path,"r")
            self.e = int(f.readline())
            self.N = int(f.readline())
            f.close()
        except:
            print(Fore.RED + "Błąd w odczycie klucza publicznego" + Fore.RESET)

        try:
            path = filepath + "-private.txt"
            f = open(path,"r")
            self.d = int(f.readline())
            f.close()
        except:
            print(Fore.RED + "Błąd w odczycie klucza prywatnego" + Fore.RESET)

    def encrypt_file(self,filepath:str,block_size = 2):
        print(Fore.CYAN + "Otwieram plik do zaszyfrowania" + Fore.RESET)

        data = ""
        try:
            f = open(filepath,"r",encoding='utf-8')
            data = f.read()
            f.close()
        except Exception as e:
            print(Fore.RED + "Wystąpił błąd\n" + Fore.RESET , e)

        print(Fore.CYAN + "Szyfruję dane" + Fore.RESET)
        try:
            path = filepath.replace(".txt","") + "-encrypted.txt"

            asc = 0
            encrypted_blocks = []
            if (len(data) > 0):
                asc = ord(data[0])
            for i in range(1 , len(data)):

                if (i % 2 == 0):
                    encrypted_blocks.append(asc)
                    asc = 0

                asc = asc * 1000 + ord(data[i])
            encrypted_blocks.append(asc)

            for i in range(len(encrypted_blocks)):
                encrypted_blocks[i] = str((encrypted_blocks[i]**self.e) % self.N)
            
            data_encrypted = " ".join(encrypted_blocks)
            f = open(path,"w+",encoding='utf-8')
            f.write(data_encrypted)
            f.close()
        except Exception as e:
            print(Fore.RED + "Wystąpił błąd\n",str(asc) + Fore.RESET , e)

    def decrypt_file(self,filepath:str,block_size = 2):
        print(Fore.CYAN + "Otwieram plik do odszyfrowania" + Fore.RESET)

        data = ""
        try:
            f = open(filepath,"r",encoding='utf-8')
            data = f.read()
            f.close()
        except Exception as e:
            print(Fore.RED + "Wystąpił błąd\n" + Fore.RESET, e)


        print(Fore.CYAN + "Deszyfruję dane" + Fore.RESET)
        try:
            path = filepath.replace(".txt","") + "-decrypted.txt"

            list_blocks = data.split(' ')
            int_blocks = []

            for s in list_blocks:
                int_blocks.append(int(s))

            data_decrypted = ""
            for i in range(len(int_blocks)):
                int_blocks[i] = (int_blocks[i]**self.d) % self.N
                
                tmp = ""
                for c in range(block_size):
                    tmp = chr(int_blocks[i] % 1000) + tmp
                    int_blocks[i] //= 1000
                data_decrypted += tmp
                
            
            f = open(path,"w+",encoding='utf-8')
            f.write(data_decrypted)
            f.close()
        except Exception as e:
            print(Fore.RED + "Wystąpił błąd\n" + Fore.RESET, e)




#main
if __name__ == '__main__':
    print(Fore.GREEN + "[RSA]\n",Fore.RESET)

    if (os.name == 'nt'):
        szyfrowanie = Szyfrowanie("dane\\klucz")
        szyfrowanie.save_key("dane\\klucz")
        szyfrowanie.encrypt_file("dane\\data1.txt")
        szyfrowanie.decrypt_file("dane\\data1-encrypted.txt")
    else:
        print(Fore.LIGHTRED_EX + "!!!Linuks lepszy!!!" + Fore.RESET)
        szyfrowanie = Szyfrowanie("dane/klucz")
        szyfrowanie.save_key("dane/klucz")
        szyfrowanie.encrypt_file("dane/data1.txt")
        szyfrowanie.decrypt_file("dane/data1-encrypted.txt")

    try:
        Beep()
        print("Koniec")
    except:
        print("Koniec")