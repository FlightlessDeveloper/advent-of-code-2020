import argparse


MANDATORY_PASSPORT_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
OPTIONAL_PASSPORT_FIELDS = {"cid"}
VALID_EYE_COLOURS = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def main():
    passports = parse_args()

    # Part 1
    valid_passports = list(filter(check_passport_fields_present, passports))
    print(f"There are {len(valid_passports)} passports with all fields")

    # Part 2
    valid_passports = list(filter(check_passport_fields_present_and_valid, passports))
    print(f"There are {len(valid_passports)} passports with all valid fields")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    passports = parse_input_lines(open(args.input_file))
    return passports


def parse_input_lines(lines):
    passports = []
    next_passport = dict()
    for l in lines:
        if len(l.strip()) < 1:
            passports.append(next_passport)
            next_passport = dict()
        else:
            for s in l.strip().split(" "):
                k, v = s.split(":")
                next_passport[k] = v
    if len(next_passport) > 0:
        passports.append(next_passport)
    return passports


def check_passport_fields_present(passport):
    for f in MANDATORY_PASSPORT_FIELDS:
        if f not in passport:
            return False
    for k in passport:
        if k not in MANDATORY_PASSPORT_FIELDS and k not in OPTIONAL_PASSPORT_FIELDS:
            return False
    return True


def check_passport_fields_present_and_valid(passport):
    if not check_passport_fields_present(passport):
        return False
    if not 1920 <= int(passport["byr"]) <= 2002:
        return False
    if not 2010 <= int(passport["iyr"]) <= 2020:
        return False
    if not 2020 <= int(passport["eyr"]) <= 2030:
        return False
    if not check_valid_height(passport["hgt"]):
        return False
    if not check_valid_hair_colour(passport["hcl"]):
        return False
    if not passport["ecl"] in VALID_EYE_COLOURS:
        return False
    if not (len(passport["pid"]) == 9 and passport["pid"].isnumeric()):
        return False
    return True


def check_valid_height(s):
    unit = s[-2:]
    value = int(s[:-2])
    if unit == "cm":
        return 150 <= value <= 193
    elif unit == "in":
        return 59 <= value <= 76
    else:
        return False


def check_valid_hair_colour(s):
    if len(s) != 7:
        return False
    if s[0] != "#":
        return False
    for c in s[1:]:
        if c not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"}:
            return False
    return True


if __name__ == "__main__":
    main()
