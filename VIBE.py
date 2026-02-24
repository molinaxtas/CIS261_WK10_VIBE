#!/usr/bin/env python3
"""
Student Grade Calculator

Features:
- Add student records (name, ID, 3 test scores)
- Automatically compute average and letter grade
- Display all students in a formatted table
- Class statistics: highest, lowest, class average
- Search students by name (case-insensitive)
- Load/save records to 'student_grades.txt' (CSV)
- Press ESC at main menu to exit
"""

import csv
import os
import sys

DATA_FILE = 'student_grades.txt'


def getch():
	"""Read a single character from stdin without echo (cross-platform)."""
	try:
		# Windows
		import msvcrt
		ch = msvcrt.getch()
		if isinstance(ch, bytes):
			return ch.decode('utf-8', 'ignore')
		return ch
	except Exception:
		# Unix
		import tty
		import termios
		fd = sys.stdin.fileno()
		old = termios.tcgetattr(fd)
		try:
			tty.setraw(fd)
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old)
		return ch


def calculate_average(scores):
	return round(sum(scores) / len(scores), 2)


def letter_grade(avg):
	if avg >= 90:
		return 'A'
	if avg >= 80:
		return 'B'
	if avg >= 70:
		return 'C'
	if avg >= 60:
		return 'D'
	return 'F'


def load_records(filename=DATA_FILE):
	students = []
	if not os.path.exists(filename):
		return students
	try:
		with open(filename, newline='') as f:
			reader = csv.DictReader(f)
			for row in reader:
				try:
					t1 = float(row.get('Test1', 0))
					t2 = float(row.get('Test2', 0))
					t3 = float(row.get('Test3', 0))
				except ValueError:
					continue
				avg = calculate_average([t1, t2, t3])
				students.append({
					'Name': row.get('Name', '').strip(),
					'ID': row.get('ID', '').strip(),
					'Test1': t1,
					'Test2': t2,
					'Test3': t3,
					'Average': avg,
					'Letter': letter_grade(avg),
				})
	except Exception:
		pass
	return students


def save_records(students, filename=DATA_FILE):
	fieldnames = ['Name', 'ID', 'Test1', 'Test2', 'Test3']
	with open(filename, 'w', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		for s in students:
			writer.writerow({
				'Name': s['Name'],
				'ID': s['ID'],
				'Test1': s['Test1'],
				'Test2': s['Test2'],
				'Test3': s['Test3'],
			})


def add_student(students):
	name = input('Student name: ').strip()
	if not name:
		print('Name cannot be empty.')
		return
	sid = input('Student ID: ').strip()
	def read_score(n):
		while True:
			try:
				val = input(f'Test {n} score (0-100): ').strip()
				v = float(val)
				if 0 <= v <= 100:
					return v
				print('Enter a number between 0 and 100.')
			except ValueError:
				print('Invalid number; try again.')

	t1 = read_score(1)
	t2 = read_score(2)
	t3 = read_score(3)
	avg = calculate_average([t1, t2, t3])
	students.append({
		'Name': name,
		'ID': sid,
		'Test1': t1,
		'Test2': t2,
		'Test3': t3,
		'Average': avg,
		'Letter': letter_grade(avg),
	})
	save_records(students)
	print(f'Student {name} added. Average: {avg}, Letter: {letter_grade(avg)}')


def display_students(students):
	if not students:
		print('No student records.')
		return
	widths = [20, 10, 8, 8, 8, 8, 6]
	hdr = f"{ 'Name':20} { 'ID':10} { 'T1':>8} { 'T2':>8} { 'T3':>8} { 'Avg':>8} { 'Grade':>6}"
	print(hdr)
	print('-' * sum(widths))
	for s in students:
		print(f"{s['Name'][:20]:20} {s['ID'][:10]:10} {s['Test1']:8.2f} {s['Test2']:8.2f} {s['Test3']:8.2f} {s['Average']:8.2f} {s['Letter']:6}")


def class_stats(students):
	if not students:
		print('No students to compute statistics.')
		return
	avgs = [s['Average'] for s in students]
	highest = max(avgs)
	lowest = min(avgs)
	class_avg = round(sum(avgs) / len(avgs), 2)
	top_students = [s for s in students if s['Average'] == highest]
	low_students = [s for s in students if s['Average'] == lowest]
	print(f'Class average: {class_avg}')
	print(f'Highest average: {highest} ({", ".join([t["Name"] for t in top_students])})')
	print(f'Lowest average: {lowest} ({", ".join([t["Name"] for t in low_students])})')


def search_student(students):
	q = input('Search name (case-insensitive): ').strip().lower()
	if not q:
		print('Empty query.')
		return
	matches = [s for s in students if q in s['Name'].lower()]
	if not matches:
		print('No matching students found.')
		return
	display_students(matches)


def main_menu():
	print('\nStudent Grade Calculator')
	print('(1) Add new student')
	print('(2) Display all students')
	print('(3) Search student by name')
	print('(4) Class statistics')
	print('(5) Save records')
	print('Press ESC to exit')
	print('Choose an option: ', end='', flush=True)


def main():
	students = load_records()
	while True:
		main_menu()
		ch = getch()
		# ESC (ASCII 27)
		if ch and ord(ch[0]) == 27:
			print('\nExiting and saving records...')
			save_records(students)
			break
		print(ch)
		if ch == '1':
			add_student(students)
		elif ch == '2':
			display_students(students)
		elif ch == '3':
			search_student(students)
		elif ch == '4':
			class_stats(students)
		elif ch == '5':
			save_records(students)
			print('Records saved.')
		else:
			print('Unknown option; press 1-5 or ESC.')


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('\nInterrupted. Saving and exiting...')
		# attempt save
		try:
			students = load_records()
			save_records(students)
		except Exception:
			pass

