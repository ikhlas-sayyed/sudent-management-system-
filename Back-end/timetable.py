import random

# Subjects and their teachers
subjects = ['Maths', 'Science', 'English', 'History', 'Geography']
teachers = ['Mr. A', 'Mr. B', 'Mr. C', 'Mr. D', 'Mr. E']

# Divisions
divisions = ['A', 'B', 'C', 'D', 'E']
daily_lectures = 7  # Number of daily lectures

# Days of the week
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

# Initialize timetable dictionary
timetable = {division: {day: None for day in days} for division in divisions}

# Assign teachers to subjects
subject_teacher_map = {subject: teacher for subject, teacher in zip(subjects, teachers)}

# Shuffle subjects and teachers to randomize assignment
random.shuffle(subjects)
random.shuffle(teachers)

# Assign subjects to divisions for each day of the week
for division in divisions:
    for day in days:
        # Create a copy of subjects and teachers for this division
        division_subjects = subjects.copy()
        division_teachers = teachers.copy()
        
        # Initialize daily timetable list
        daily_timetable = []
        
        for period in range(daily_lectures):
            # If there are no subjects left for this division, repeat subjects
            if not division_subjects:
                division_subjects = subjects.copy()  # Reset division subjects
            
            # Randomly select a subject and its teacher
            selected_subject = random.choice(division_subjects)
            selected_teacher = subject_teacher_map[selected_subject]
            
            # Add subject and teacher to daily timetable
            daily_timetable.append(f"{selected_subject} - {selected_teacher}")
            
            # Remove assigned subject from division_subjects
            division_subjects.remove(selected_subject)
            
            # Remove assigned teacher from division_teachers if present
            if selected_teacher in division_teachers:
                division_teachers.remove(selected_teacher)
            
            # Update division_teachers to ensure each teacher teaches only one subject
            division_teachers = [teacher for teacher in division_teachers if teacher != selected_teacher]
        
        # Assign daily timetable to the division's timetable
        timetable[division][day] = daily_timetable

# Create HTML files with styled timetables for each division for the week
for division, timetable_data in timetable.items():
    with open(f"{division}_weekly_timetable.html", "w") as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html>\n")
        f.write("<head>\n")
        f.write(f"<title>{division} Weekly Timetable</title>\n")
        
        # Add CSS styles
        f.write("<style>\n")
        f.write("body { font-family: Arial, sans-serif; margin: 20px; }\n")
        f.write("h1 { text-align: center; }\n")
        f.write("table { width: 100%; border-collapse: collapse; margin: 20px auto; }\n")
        f.write("th, td { padding: 10px; border: 1px solid black; text-align: center; }\n")
        f.write("th { background-color: #f2f2f2; }\n")
        f.write("</style>\n")
        
        f.write("</head>\n")
        f.write("<body>\n")
        f.write(f"<h1>Division {division} Weekly Timetable</h1>\n")
        
        # Write timetable data as a single table
        f.write("<table>\n")
        f.write("<tr><th>Period/Day</th>")
        
        for day in days:
            f.write(f"<th>{day}</th>")
        
        f.write("</tr>\n")
        
        # Generate rows for each period
        for period in range(daily_lectures):
            f.write(f"<tr><td>Period {period+1}</td>")
            
            for day in days:
                f.write(f"<td>{timetable_data[day][period]}</td>")
            
            f.write("</tr>\n")
        
        f.write("</table>\n")
        f.write("</body>\n")
        f.write("</html>")
