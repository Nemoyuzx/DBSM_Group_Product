from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# 一、人员与地址层

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    line1 = models.CharField(max_length=120, null=False)
    line2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=60, null=False)
    province = models.CharField(max_length=60, null=False)
    postal_code = models.CharField(max_length=20, null=False)
    country = models.CharField(max_length=60, null=False)
    # Django不直接支持Point类型，这里简化为经纬度字段
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    def __str__(self):
        return f"{self.line1}, {self.city}, {self.province}"

class Person(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Undefined'),
    ]
    
    person_id = models.AutoField(primary_key=True)
    legal_name = models.CharField(max_length=100, null=False)
    preferred_name = models.CharField(max_length=100, null=False)
    sex_at_birth = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False)
    gender_identity = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(null=False)
    national_id = models.CharField(max_length=30, unique=True, null=False)
    primary_address_id = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)

    def __str__(self):
        return f"{self.legal_name} ({self.person_id})"

class Student(models.Model):
    ENROLLMENT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('leave', 'Leave'),
        ('graduate', 'Graduate'),
        ('dismissed', 'Dismissed'),
    ]
    
    student_id = models.OneToOneField(Person, primary_key=True, on_delete=models.CASCADE)
    admission_year = models.SmallIntegerField(null=False)
    enrollment_status = models.CharField(max_length=10, choices=ENROLLMENT_STATUS_CHOICES, null=False)
    expected_grad_term = models.CharField(max_length=6, null=False)
    disability_flag = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Student {self.student_id}"

class Staff(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('adjunct', 'Adjunct'),
        ('GTA', 'GTA'),
    ]
    
    STAFF_STATUS_CHOICES = [
        ('active', 'Active'),
        ('leave', 'Leave'),
        ('retired', 'Retired'),
    ]
    
    staff_id = models.OneToOneField(Person, primary_key=True, on_delete=models.CASCADE)
    hire_date = models.DateField(null=False)
    employment_type = models.CharField(max_length=10, choices=EMPLOYMENT_TYPE_CHOICES, null=False)
    staff_status = models.CharField(max_length=10, choices=STAFF_STATUS_CHOICES, null=False)
    
    def __str__(self):
        return f"Staff {self.staff_id}"

class RewardPunish(models.Model):
    remark_id = models.BigAutoField(primary_key=True)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    remark_type = models.CharField(max_length=20, null=False)
    remark_value = models.CharField(max_length=200, null=False)
    updated_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.remark_type}: {self.person_id}"

class Term(models.Model):
    term_code = models.CharField(max_length=6, primary_key=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    description = models.CharField(max_length=60, null=True, blank=True)
    is_current_term = models.BooleanField(default=False)
    
    def __str__(self):
        return self.term_code

class AcademicRank(models.Model):
    rank_id = models.SmallIntegerField(primary_key=True)
    rank_name = models.CharField(max_length=50, null=False)
    
    def __str__(self):
        return self.rank_name

class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    inst_id = models.ForeignKey('Institution', on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=False)
    phone = models.CharField(max_length=20, null=True, blank=True)
    office_location = models.CharField(max_length=100, null=False)
    chair_staff_id = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.name

class InstructorRole(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, primary_key=True)
    academic_rank = models.ForeignKey(AcademicRank, on_delete=models.CASCADE)
    primary_dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    primary_dept_name = models.CharField(max_length=100, null=True, blank=True)
    start_term_code = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='instructor_start_terms')
    end_term_code = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True, related_name='instructor_end_terms')
    
    def __str__(self):
        return f"{self.staff_id} - {self.primary_dept_name}"

class AdminPosition(models.Model):
    position_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60, null=False)
    level = models.CharField(max_length=10, null=False, choices=[
        ('school', 'School'),
        ('department', 'Department'),
        ('program', 'Program'),
    ])
    
    def __str__(self):
        return self.title

class AdminRole(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    position_id = models.ForeignKey(AdminPosition, on_delete=models.CASCADE)
    start_term_code = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='admin_start_terms')
    end_term_code = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True, related_name='admin_end_terms')
    
    class Meta:
        unique_together = ('staff_id', 'position_id')
    
    def __str__(self):
        return f"{self.staff_id} - {self.position_id.title}"

class NameHistory(models.Model):
    history_id = models.BigAutoField(primary_key=True)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    old_name = models.CharField(max_length=100, null=False)
    new_name = models.CharField(max_length=100, null=False)
    effective_to = models.DateField(null=True, blank=True)
    changed_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.person_id}: {self.old_name} -> {self.new_name}"

class AccommodationType(models.Model):
    acc_type = models.CharField(max_length=10, primary_key=True)
    description = models.CharField(max_length=100, null=False)
    
    def __str__(self):
        return self.acc_type

class DisabilityAccommodation(models.Model):
    acc_id = models.BigAutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    acc_type = models.ForeignKey(AccommodationType, on_delete=models.CASCADE)
    active_from = models.DateField(null=False)
    active_to = models.DateField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student_id}: {self.acc_type}"

# 二、学术组织层

class Institution(models.Model):
    TYPE_CHOICES = [
        ('main', 'Main'),
        ('branch', 'Branch'),
        ('partner', 'Partner'),
        ('online', 'Online'),
    ]
    
    inst_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, null=False)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=False)
    accreditation_level = models.CharField(max_length=30, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Program(models.Model):
    DEGREE_TYPE_CHOICES = [
        ('BA', 'BA'),
        ('BSc', 'BSc'),
        ('MSc', 'MSc'),
        ('MEng', 'MEng'),
        ('PhD', 'PhD'),
        ('Integrated', 'Integrated'),
    ]
    
    program_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, null=False)
    degree_type = models.CharField(max_length=10, choices=DEGREE_TYPE_CHOICES, null=False)
    credit_required = models.SmallIntegerField(null=False)
    gpa_min_required = models.DecimalField(max_digits=3, decimal_places=2, null=False, 
                                          validators=[MinValueValidator(2.0)])
    
    def __str__(self):
        return f"{self.name} ({self.degree_type})"

class ProgramAffiliation(models.Model):
    AFFILIATION_TYPE_CHOICES = [
        ('host', 'Host'),
        ('co-host', 'Co-host'),
    ]
    
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    affiliation_type = models.CharField(max_length=10, choices=AFFILIATION_TYPE_CHOICES, null=False)
    
    class Meta:
        unique_together = ('program_id', 'dept_id')
    
    def __str__(self):
        return f"{self.program_id} - {self.dept_id}: {self.affiliation_type}"

class StudentProgram(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE)
    is_primary_major = models.BooleanField(default=True)
    start_term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='student_program_starts')
    end_term = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True, related_name='student_program_ends')
    
    class Meta:
        unique_together = ('student_id', 'program_id')
    
    def __str__(self):
        return f"{self.student_id}: {self.program_id}"

class Class(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('merged', 'Merged'),
        ('dissolved', 'Dissolved'),
    ]
    
    MODE_CHOICES = [
        ('on-campus', 'On-campus'),
        ('online', 'Online'),
        ('mixed', 'Mixed'),
    ]
    
    class_id = models.AutoField(primary_key=True)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    cohort_year = models.SmallIntegerField(null=False)
    class_name = models.CharField(max_length=60, null=False)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False)
    note_json = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.class_name} ({self.cohort_year})"

class StudentClass(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    start_term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='student_class_starts')
    end_term = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True, related_name='student_class_ends')
    role_in_class = models.CharField(max_length=20, null=True, blank=True)
    
    class Meta:
        unique_together = ('student_id', 'class_id')
    
    def __str__(self):
        return f"{self.student_id}: {self.class_id}"

class ClassAdvisor(models.Model):
    ADVISOR_ROLE_CHOICES = [
        ('academic', 'Academic'),
        ('mental', 'Mental'),
        ('career', 'Career'),
        ('deputy', 'Deputy'),
    ]
    
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    advisor_role = models.CharField(max_length=10, choices=ADVISOR_ROLE_CHOICES, null=False)
    start_term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='advisor_start_terms')
    end_term = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True, related_name='advisor_end_terms')
    is_primary = models.BooleanField(default=True)
    note = models.CharField(max_length=120, null=True, blank=True)
    
    class Meta:
        unique_together = ('class_id', 'staff_id')
    
    def __str__(self):
        return f"{self.staff_id}: {self.class_id} ({self.advisor_role})"

# 三、课程体系层

class Course(models.Model):
    GRADING_SCHEME_CHOICES = [
        ('letter', 'Letter'),
        ('percent', 'Percent'),
        ('passfail', 'Pass/Fail'),
    ]
    
    LANGUAGE_CHOICES = [
        ('CN', 'Chinese'),
        ('EN', 'English'),
        ('BI', 'Bilingual'),
    ]
    
    course_code = models.CharField(max_length=15, primary_key=True)
    title = models.CharField(max_length=120, null=False)
    credit_value = models.DecimalField(max_digits=3, decimal_places=1, null=False)
    owning_dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    default_grading_scheme = models.CharField(max_length=10, choices=GRADING_SCHEME_CHOICES, null=False)
    syllabus_blob = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null=False)
    canonical_flag = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.course_code}: {self.title}"

class CourseRequisite(models.Model):
    CR_id = models.CharField(max_length=15, primary_key=True)
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='requisites')
    prereq_code = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='required_for')
    min_grade_required = models.CharField(max_length=4, null=True, blank=True)
    concurrent_allowed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.course_code} requires {self.prereq_code}"

class CourseOffering(models.Model):
    DELIVERY_MODE_CHOICES = [
        ('in-person', 'In-person'),
        ('online', 'Online'),
        ('hybrid', 'Hybrid'),
        ('self-paced', 'Self-paced'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('waitlist', 'Waitlist'),
        ('cancelled', 'Cancelled'),
        ('merged', 'Merged'),
    ]
    
    offering_id = models.BigAutoField(primary_key=True)
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE)
    term_code = models.ForeignKey(Term, on_delete=models.CASCADE)
    section_number = models.CharField(max_length=5, null=False)
    delivery_mode = models.CharField(max_length=10, choices=DELIVERY_MODE_CHOICES, null=False)
    campus = models.CharField(max_length=40, null=False)
    room_id = models.CharField(max_length=20, null=True, blank=True)
    capacity = models.SmallIntegerField(null=False)
    waitlist_capacity = models.SmallIntegerField(default=0)
    cross_list_group = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False)
    duration_terms = models.SmallIntegerField(default=1)
    
    class Meta:
        unique_together = ('course_code', 'term_code', 'section_number')
    
    def __str__(self):
        return f"{self.course_code} - {self.term_code} ({self.section_number})"

class TeachAssignment(models.Model):
    ROLE_CHOICES = [
        ('lead', 'Lead'),
        ('co', 'Co-instructor'),
        ('TA', 'Teaching Assistant'),
        ('industrymentor', 'Industry Mentor'),
    ]
    
    offering_id = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, null=False)
    pay_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    class Meta:
        unique_together = ('offering_id', 'staff_id')
    
    def __str__(self):
        return f"{self.staff_id} - {self.offering_id} ({self.role})"

class ClassCoursePlan(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    offering_id = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    compulsory_flag = models.BooleanField(null=False)
    planned_week = models.SmallIntegerField(null=True, blank=True)
    remark = models.CharField(max_length=120, null=True, blank=True)
    
    class Meta:
        unique_together = ('class_id', 'offering_id')
    
    def __str__(self):
        return f"{self.class_id} - {self.offering_id}"

# 四、注册与成绩层

class Enrollment(models.Model):
    ENROLL_STATE_CHOICES = [
        ('added', 'Added'),
        ('waitlist', 'Waitlist'),
        ('dropped', 'Dropped'),
        ('audit', 'Audit'),
        ('waived', 'Waived'),
    ]
    
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    offering_id = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    enroll_state = models.CharField(max_length=10, choices=ENROLL_STATE_CHOICES, null=False)
    enroll_date = models.DateField(null=False)
    drop_date = models.DateField(null=True, blank=True)
    grade_final = models.CharField(max_length=4, null=True, blank=True)
    grade_points = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    repeat_flag = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('student_id', 'offering_id')
    
    def __str__(self):
        return f"{self.student_id} - {self.offering_id}"

class EnrollmentOverride(models.Model):
    OVERRIDE_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('prereq', 'Prerequisite'),
    ]
    
    override_id = models.BigAutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    offering_id = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    override_type = models.CharField(max_length=10, choices=OVERRIDE_TYPE_CHOICES, null=False)
    reason = models.TextField(null=False)
    approved_by = models.ForeignKey(Staff, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.student_id} - {self.offering_id} ({self.override_type})"

class AssessmentItem(models.Model):
    item_id = models.BigAutoField(primary_key=True)
    offering_id = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=60, null=False)
    weight_percent = models.DecimalField(max_digits=5, decimal_places=2, null=False, 
                                        validators=[MinValueValidator(0), MaxValueValidator(100)])
    due_datetime = models.DateTimeField(null=False)
    allow_multiple_attempts = models.BooleanField(default=False)
    max_attempts = models.SmallIntegerField(default=1, validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"{self.offering_id} - {self.item_name}"

class AssessmentSubmission(models.Model):
    submission_id = models.BigAutoField(primary_key=True)
    item_id = models.ForeignKey(AssessmentItem, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    attempt_no = models.SmallIntegerField(validators=[MinValueValidator(1)])
    submit_time = models.DateTimeField(auto_now_add=True)
    score_raw = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    file_link = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        unique_together = ('item_id', 'student_id', 'attempt_no')
    
    def __str__(self):
        return f"{self.student_id} - {self.item_id} (Attempt {self.attempt_no})"

class AssessmentFeedback(models.Model):
    FEEDBACK_TYPE_CHOICES = [
        ('text', 'Text'),
        ('rubric', 'Rubric'),
    ]
    
    feedback_id = models.BigAutoField(primary_key=True)
    submission_id = models.ForeignKey(AssessmentSubmission, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=10, choices=FEEDBACK_TYPE_CHOICES, null=False)
    content = models.JSONField(null=False)
    
    def __str__(self):
        return f"Feedback for {self.submission_id}"

class GradeAppeal(models.Model):
    DECISION_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    
    appeal_id = models.BigAutoField(primary_key=True)
    item_id = models.ForeignKey(AssessmentItem, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    appeal_date = models.DateField(auto_now_add=True)
    appeal_reason = models.TextField(null=False)
    decision = models.CharField(max_length=10, choices=DECISION_CHOICES, null=False, default='pending')
    resolved_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    resolution_note = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student_id} - {self.item_id} ({self.decision})"

# 五、学籍与合规层

class LeaveReason(models.Model):
    reason_code = models.CharField(max_length=10, primary_key=True)
    description = models.CharField(max_length=100, null=False)
    
    def __str__(self):
        return self.description

class LeaveOfAbsence(models.Model):
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    
    loa_id = models.BigAutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='leave_start_terms')
    end_term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='leave_end_terms')
    reason_code = models.ForeignKey(LeaveReason, on_delete=models.CASCADE)
    approval_status = models.CharField(max_length=10, choices=APPROVAL_STATUS_CHOICES, null=False)
    approved_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    documentation_link = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=60, null=False)
    
    def __str__(self):
        return f"{self.student_id} - {self.start_term} to {self.end_term}"

class ExchangeEnrollment(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    exch_id = models.BigAutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    host_inst_id = models.ForeignKey(Institution, on_delete=models.CASCADE)
    host_program_id = models.CharField(max_length=120, null=True, blank=True)
    host_term_code = models.ForeignKey(Term, on_delete=models.CASCADE)
    credit_load = models.DecimalField(max_digits=4, decimal_places=1, null=False)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, null=False)
    transcript_received_flag = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student_id} - {self.host_inst_id} ({self.host_term_code})"

class TransferredCredit(models.Model):
    tc_id = models.BigAutoField(primary_key=True)
    exch_id = models.ForeignKey(ExchangeEnrollment, on_delete=models.CASCADE)
    host_course_code = models.CharField(max_length=20, null=False)
    host_grade = models.CharField(max_length=8, null=False)
    host_credit = models.DecimalField(max_digits=4, decimal_places=1, null=False)
    mapped_course_code = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    credit_accepted = models.DecimalField(max_digits=4, decimal_places=1, null=False)
    decision_by = models.ForeignKey(Staff, on_delete=models.CASCADE)
    decision_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.exch_id} - {self.host_course_code}"

class CourseWaiverRequest(models.Model):
    REASON_TYPE_CHOICES = [
        ('placement-test', 'Placement Test'),
        ('competency', 'Competency'),
        ('certificate', 'Certificate'),
    ]
    
    DECISION_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    
    waiver_id = models.BigAutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE)
    reason_type = models.CharField(max_length=20, choices=REASON_TYPE_CHOICES, null=False)
    evidence_link = models.CharField(max_length=200, null=True, blank=True)
    request_date = models.DateField(auto_now_add=True)
    decision = models.CharField(max_length=10, choices=DECISION_CHOICES, null=False, default='pending')
    decision_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    decision_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student_id} - {self.course_code} ({self.decision})"

class InstructorLeave(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('sabbatical', 'Sabbatical'),
        ('parental', 'Parental'),
        ('sick', 'Sick'),
    ]
    
    leave_id = models.BigAutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_start_term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='instructor_leave_starts')
    leave_end_term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='instructor_leave_ends')
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES, null=False)
    replacement_required_flag = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.staff_id} - {self.leave_start_term} to {self.leave_end_term}"

class AcademicIncident(models.Model):
    incident_id = models.BigAutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    offering_id = models.ForeignKey(CourseOffering, on_delete=models.SET_NULL, null=True)
    incident_type = models.CharField(max_length=40, null=False)
    report_date = models.DateField(null=False)
    status = models.CharField(max_length=20, null=False)
    penalty_description = models.TextField(null=True, blank=True)
    recorded_by = models.ForeignKey(Staff, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.student_id} - {self.incident_type}"

# 六、创新与能力层

class Competency(models.Model):
    comp_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=120, null=False)
    level_scale = models.JSONField()
    linked_course_code = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.description

class StudentCompetency(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    comp_id = models.ForeignKey(Competency, on_delete=models.CASCADE)
    competency_level = models.CharField(max_length=10, null=False)
    evidence_link = models.CharField(max_length=200, null=True, blank=True)
    verified_by = models.ForeignKey(Staff, on_delete=models.CASCADE)
    verify_date = models.DateField(null=False)
    
    class Meta:
        unique_together = ('student_id', 'comp_id')
    
    def __str__(self):
        return f"{self.student_id} - {self.comp_id} ({self.competency_level})"

class LearningEvent(models.Model):
    event_id = models.BigAutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=30, null=False)
    timestamp = models.DateTimeField(null=False)
    metadata_json = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student_id} - {self.offering} ({self.event_type})"

class ProjectTeam(models.Model):
    team_id = models.BigAutoField(primary_key=True)
    project_title = models.CharField(max_length=120, null=False)
    advisor_staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.project_title} ({self.team_id})"

class TeamMember(models.Model):
    team_id = models.ForeignKey(ProjectTeam, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    role_in_team = models.CharField(max_length=20, null=True, blank=True)
    join_date = models.DateField(null=False)
    
    class Meta:
        unique_together = ('team_id', 'student_id')
    
    def __str__(self):
        return f"{self.student_id} in {self.team_id}"
