import csv
from datetime import datetime, date
from statistics import mean, stdev


def new_blood_test():
    """
    Generate and return a BloodTest object.

    Asks user to type values for every BloodTest field, informing which field is being set at the moment

    Returns
    -------
    blood_test : BloodTest
        New, specified by user blood test
    """
    blood_test = BloodTest("0", "0", "0", datetime.now())
    blood_test.sys_pressure = input("Ciśnienie skurczowe: ")
    blood_test.dias_pressure = input("Ciśnienie rozkurczowe: ")
    blood_test.heart_rate = input("Tętno: ")
    test_date = input(
        "Data pomiaru w formacie DD-MM-YYYY lub wciśnij [Enter] aby zachować dzisiejszy dzień: ") or datetime.strftime(
        datetime.now(), '%d-%m-%Y')
    test_time = input(
        "Czas pomiaru w formacie HH:MM lub wciśnij [Enter] aby zachować aktualną godzinę: ") or datetime.strftime(
        datetime.now(), '%H:%M')
    blood_test.test_datetime = " ".join([test_date, test_time])
    return blood_test


def get_date_range_input():
    """
    Create and return date range.

    Asks user to specify the starting and ending dates of the period.
    Providing no input in each case sets the date to earliest: date.Min or latest possible: date.today().
    If user makes mistake in input, returns earliest and latest possible values.

    Returns
    -------
    range_start, range_end : tuple of date
        Tuple containing start and end of period

    """
    try:
        start = input(
            "Początek zakresu dat[DD-MM-YYYY], wciśnij [Enter] aby zostawić brak ograniczeń: ") or datetime.strftime(
            datetime.min, "%d-%m-%Y")  # start date in string format
        range_start = datetime.strptime(start, "%d-%m-%Y").date()
        if range_start > date.today():
            raise ValueError("Początek zakresu nie może być późniejszy od dzisiejszej daty")
        end = input(
            "Koniec zakresu dat[DD-MM-YYYY], wciśnij [Enter] aby zostawić brak ograniczeń: ") or datetime.strftime(
            datetime.today(), "%d-%m-%Y")  # end date in string format
        range_end = datetime.strptime(end, "%d-%m-%Y").date()
        if range_end < range_start:
            raise ValueError("Koniec zakresu nie może być wcześniej niż początek zakresu")
        return range_start, range_end
    except ValueError as e:  # In case user provides incorrect data format
        print(e)
        return date.min, date.today()


class BloodTest:
    """
    A class used to represent single blood pressure and heart rate test.

    Attributes
    ----------
    sys_pressure : int
        systolic pressure
    dias_pressure : int
        diastolic pressure
    heart_rate : int
        heart rate
    test_datetime : datetime
            date and hour of performed test in format DD-MM-YYYY HH:MM

    Methods
    -------
    edit()
        Change values in single blood test.
    parameters()
        Return list of parameters BloodTest is describing.
    """
    COLUMN_WIDTH = 22

    def __init__(self, sys, dias, hr, test_datetime):
        """
        Parameters
        ----------
        sys : string
            systolic pressure
        dias : string
            diastolic pressure
        hr : string
            heart rate
        test_datetime : string,datetime
            date and hour of performed test in format DD-MM-YYYY HH:MM or datetime object
        """
        try:
            self.sys_pressure = sys
            self.dias_pressure = dias
            self.heart_rate = hr
            self.test_datetime = test_datetime
        except ValueError as e:
            print(e)

    @property
    def sys_pressure(self):
        """
        Get systolic pressure.

        Returns
        -------
        int
            systolic pressure of test
        """
        return self._sys_pressure

    @sys_pressure.setter
    def sys_pressure(self, value):
        """
        Set systolic pressure.

        Parameters
        ----------
        value : string
        """
        if not value.isdigit() or int(value) < 0:
            print("Wartość ciśnienia rozkurczowego powinna być liczbą naturalną")
            self.sys_pressure = input("Podaj wartość jeszcze raz: ")
        else:
            self._sys_pressure = int(value)

    @property
    def dias_pressure(self):
        """
        Get diastolic pressure.

        Returns
        -------
        int
            diastolic pressure of test
        """
        return self._dias_pressure

    @dias_pressure.setter
    def dias_pressure(self, value):
        """
        Set diastolic pressure.

        Parameters
        ----------
        value : string
        """
        if not value.isdigit() or int(value) < 0:
            print("Wartość ciśnienia rozkurczowego powinna być liczbą naturalną")
            self.dias_pressure = input("Podaj wartość jeszcze raz: ")
        else:
            self._dias_pressure = int(value)

    @property
    def heart_rate(self):
        """
        Get heart rate.

        Returns
        -------
        int
            heart rate of test
        """
        return self._heart_rate

    @heart_rate.setter
    def heart_rate(self, value):
        """
        Set heart rate.

        Parameters
        ----------
        value : string
        """
        if not value.isdigit() or int(value) < 0:
            print("Tętno powinno być liczbą naturalną")
            self.heart_rate = input("Podaj wartość jeszcze raz: ")
        else:
            self._heart_rate = int(value)

    @property
    def test_datetime(self):
        """
        Get datetime.

        Returns
        -------
        datetime
            datetime of test
        """
        return self._test_datetime

    @test_datetime.setter
    def test_datetime(self, value):
        """
        Set datetime.

        If providing string expected format is DD-MM-YYYY HH:MM.

        Parameters
        ----------
        value : datetime, string
        """
        if isinstance(value, datetime):
            self._test_datetime = value
            return
        try:
            self._test_datetime = datetime.strptime(value, "%d-%m-%Y %H:%M")
        except ValueError:
            print(f"{value} nie jest zgodna z %d-%m-%Y %H:%M")
            test_date = input(f"dzień pomiaru w formacie DD-MM-YYYY: ")
            test_time = input(f"czas pomiaru w formacie HH:MM: ")
            self.test_datetime = " ".join([test_date, test_time])

    def edit(self):
        """
        Edit blood pressure test

        Ask user to provide new or leave old value in every field of blood pressure test
        """
        print("Jeżeli chcesz pozostawić wartość parametru, kliknij [ENTER]")
        self.sys_pressure = input(f"ciśnienie skurczowe [{self.sys_pressure}]: ") or str(self.sys_pressure)
        self.dias_pressure = input(f"ciśnienie rozkurczowe [{self.dias_pressure}]: ") or str(self.dias_pressure)
        self.heart_rate = input(f"tętno [{self.heart_rate}]: ") or str(self.heart_rate)
        old_date = datetime.strftime(self.test_datetime, '%d-%m-%Y')
        old_time = datetime.strftime(self.test_datetime, '%H:%M')
        test_date = input(f"dzień pomiaru w formacie DD-MM-YYYY [{old_date}]: ") or old_date
        test_time = input(f"czas pomiaru w formacie HH:MM [{old_time}]: ") or old_time
        self.test_datetime = " ".join([test_date, test_time])

    def parameters(self):
        """Return list of parameters BloodTest is describing."""
        return [self.sys_pressure, self.dias_pressure, self.heart_rate, self.test_datetime.strftime("%d-%m-%Y %H:%M")]

    def __lt__(self, other):
        """
        Compare two BloodTest elements

        BloodTest1 is considered less than BloodTest2 when it's test_datetime precedes other's test_datetime in time

        Parameters
        -----------
        other : BloodTest

        Returns
        -------
        bool
            True is BloodTest precedes other BloodTest in time, False if not
        """
        return self.test_datetime < other.test_datetime

    def __str__(self):
        """Return BloodTest string representation to show in table"""
        result = ""
        for elem in self.parameters():
            result += f"{elem}".center(self.COLUMN_WIDTH)
        return result


class BloodTestsManager:
    """
    A class used to store, manage and extract information from blood pressure tests.

    Attributes
    ----------
    blood_tests : list of BloodTest, sorted
    headers : list of string
        List containing strings of BloodTest fields and "number of test", used for displaying data
    COLUMN_WIDTH : int
        single column width

    Methods
    -------
    show_blood_tests(start=0)
        Display blood pressure tests
    new_blood_test()
        Create new blood pressure test
    manage_blood_tests()
        Delete or edit blood pressure test
    show_stats(range_start=date.min, range_end=date.today())
        Show statistics of blood tests in period
    print_headers(is_no_id=0)
        Display headers
    save()
        Save blood pressure tests to file
    read()
        Read blood pressure tests from file
    """
    def __init__(self):
        """
        Initialize a blood test manager.

        Creates an empty list for blood pressure tests, prepares headers for displaying data, sets fixed column width
        """
        self.blood_tests = []
        self.headers = ["Numer pomiaru", "Ciśnienie skurczowe", "Ciśnienie rozkurczowe", "Tętno serca",
                        "Godzina pomiaru"]
        self.COLUMN_WIDTH = 22
        BloodTest.COLUMN_WIDTH = self.COLUMN_WIDTH

    def show_blood_tests(self, start=0):
        """
        Display blood pressure in a table.

        Displays five blood pressure tests from blood_tests list, depending on position in this list.
        Allows user to run function again with moved starting point

        Parameters
        ----------
        start : int, default 0
            Position in list of first blood pressure test to display
        """
        step = 5  # Number of records displayed
        end = min(start + step, len(self.blood_tests))
        if start > len(self.blood_tests):  # Cant display elements after last element in the list
            return
        print(f"Pomiary o numerach od: {start} do {end}, z {len(self.blood_tests)}")
        self.print_headers()
        for i, blood_test in enumerate(self.blood_tests[start:end], start=start):
            print(f"{i + 1}".center(BloodTest.COLUMN_WIDTH), end="")
            print(blood_test)
        if len(self.blood_tests) > start + step:
            action = input("""Aby zobaczyć kolejne pomiary wpisz dowolny znak i zatwierdź [ENTER]: 
Aby wrócić wciśnij [ENTER]: """)
            if action != "":
                self.show_blood_tests(start + step)
            return

    def new_blood_test(self):
        """
        Create new blood pressure test and add it to list.

        Creates new blood pressure test using new_blood_test() function, adds it to blood_tests list,
        sorts the list and saves it to the file. Displays new record.
        """
        new_test = new_blood_test()
        self.blood_tests.append(new_test)
        self.blood_tests.sort()
        self.save()
        print("Dodano nowy pomiar ciśnienia krwi: ")
        self.print_headers(1)
        print(new_test)

    def manage_blood_tests(self):
        """
        Delete or edit blood pressure test.

        Asks user to provide blood pressure test position in tests list, if found asks user to choose between
        deleting or editing record. If editing chosen, calls edit() function on blood test and then display
        new record.
        """
        i = int(input("Proszę podać numer pomiaru(lub 0 aby wrócić), znajdziesz go w zakładce \"Pokaż pomiary\": "))
        if i == 0:
            return
        if i not in range(1, len(self.blood_tests) + 1):
            print("Nie ma takiego numeru pomiaru")
            return
        print("Znaleziono pomiar:")
        self.print_headers()
        print(f"{i}".center(BloodTest.COLUMN_WIDTH), end="")
        print(self.blood_tests[i - 1])
        action = input("1 - usunięcie\n2 - edycja\nCo chcesz zrobić z pomiarem: ")
        if action == "1":
            self.blood_tests.pop(i - 1)
            self.save()
            print("Pomyślnie sunięto pomiar\n")
        elif action == "2":
            try:
                self.blood_tests[i - 1].edit()
                self.blood_tests.sort()
                self.save()
                print("Edytowano pomiar ciśnienia krwi: ")
                self.print_headers()
                print(f"{i}".center(BloodTest.COLUMN_WIDTH), end="")
                print(self.blood_tests[i - 1])
            except ValueError:
                print("Niepowodzenie, wprowadzono nieprawidłową wartość")

    def show_stats(self, range_start=date.min, range_end=date.today()):
        """
        Display statistics connected with stored data.

        Displays Max, Min, Mean, Standard deviation of records within period specified in range_start and range_end.
        Allows to choose another period and display statistics for it.

        Parameters
        ----------
        range_start : date
        range_end : date
        """
        values = zip(
            *[test.parameters()[0:3] for test in self.blood_tests if
              range_start <= test.test_datetime.date() <= range_end])
        # Take systolic and diastolic pressure and heart rate from every record in specified range as list,
        # unpack it to have lists, zip it to create tuples of every parameter in all records
        values_list = list(values)  # [(sys1,..., sysN), (dias1,...,diasN), (hr1,...,hrN)]
        if values_list:  # if any record found
            len_values = len(values_list[0])
            if len_values == 1:  # if only one record standard deviation cannot be caluclated
                stats = [[*elem, *elem, *elem, 0] for elem in values_list]
            else:
                stats = [[max(elem), min(elem), mean(elem), stdev(elem)] for elem in values_list]

            print(f"Dane z zakresu dat: od {range_start} do {range_end}, {len_values} pomiarów")
            for header in ["", "Max", "Min", "Średnia", "Odchylenie standardowe"]:
                print(f"{header}".center(BloodTest.COLUMN_WIDTH), end="")
            print()
            for i, elems in enumerate(stats):
                print(f"{self.headers[i + 1]}".center(BloodTest.COLUMN_WIDTH), end="")
                for elem in elems:
                    print(f"{elem:.2f}".center(BloodTest.COLUMN_WIDTH), end="")
                print()
        else:
            print("Brak wyników")
            return
        print("Wciśnij dowolny klawisz i zatwierdź [Enter] - dane z innego okresu\n[Enter] - Powrót")
        action = input("Wybierz akcję: ")
        if action != "":
            self.show_stats(*get_date_range_input())

    def print_headers(self, is_no_id=0):
        """Display headers in column-style."""
        for header in self.headers[is_no_id:]:
            print(f"{header}".center(BloodTest.COLUMN_WIDTH), end="")
        print()

    def save(self):
        """Save data to csv file."""
        with open("measurements.csv", "w", newline='') as f:
            writer = csv.writer(f)
            for blood_test in self.blood_tests:
                writer.writerow(blood_test.parameters())

    def read(self):
        """Read data from csv file."""
        try:
            with open("measurements.csv", "r", newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    self.blood_tests.append(BloodTest(row[0], row[1], row[2], row[3]))
        except FileNotFoundError:
            print("Nie znaleziono pliku z danymi wcześniejszych pomiarów, utworzony zostanie nowy plik")
        except IndexError:
            print("Nie znaleziono żadnych pomiarów w pliku")


class Menu:
    """
    A class used to run BloodTestManager instance and call its methods.

    Attributes
    ----------
    manager : BloodTestsManager
        Blood test manager Menu is going to control

    Methods
    -------
    run()
        Run interactive menu to communicate with user
    """
    def __init__(self):
        """Initialize BloodTestManager and make it read data from file"""
        self.manager = BloodTestsManager()
        self.manager.read()

    def run(self):
        """
        Run interactive menu to communicate with user.

        Displays menu options, calls BloodTestManager method by users choice

        Methods
        -------
        ask_action()
            Displays menu options for user
        """
        print("Witamy w dzienniczku badań ciśnienia krwi")

        def ask_action():
            """
            Display menu options.

            Returns
            -------
            action : string
                Single character assigned to specific method
            """
            print("""1 - Pokaż pomiary
2 - Dodaj nowy pomiar
3 - Zarządzaj pomiarami
4 - Statystyki
5 - Wyjdz""")
            return input("Podaj numer akcji: ")

        action = ask_action()
        while action != "5":
            match action:
                case "1":
                    self.manager.show_blood_tests()
                case "2":
                    self.manager.new_blood_test()
                case "3":
                    self.manager.manage_blood_tests()
                case "4":
                    self.manager.show_stats()
                case _:
                    print("Nie rozpoznano akcji, upewnij się, że wybrałeś cyfrę z zakresu 1-4")
            action = ask_action()
        self.manager.save()


if __name__ == '__main__':
    app = Menu()
    app.run()
