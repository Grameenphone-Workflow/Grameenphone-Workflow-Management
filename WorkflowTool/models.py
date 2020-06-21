from django.db import models

# create your models here.

OBDG = "Onboarding"
PRQ = "Product Requistion"

PASSED = "Passed"
FAILED = "Failed"
PENDING = "Pending"

PRIME = "Prime Account"
SLA = "Strategic and Large Account"
EA = "Emerging Accounts"
GA = "Government Accounts"

COCP = "COCP"
COIP = "COIP"

WORKFLOW_TYPES = [
        (OBDG, "Onboarding"),
        (PRQ, "Product Requisition"),
    ]

STATUSES = [
    (PASSED, "Passed"),
    (FAILED, "Failed"),
    (PENDING, "Pending"),
]

SUBSEGMENTS = [
    (PRIME, "Prime Accounts"),
    (SLA, "Strategic and Large Accounts"),
    (EA, "Emerging Accounts"),
    (GA, "Government Accounts"),
]

CORPORATE_TYPES = [
    (COCP, "COCP"),
    (COIP, "COIP"),
]

LOCATIONS = [
    ("GPHouse", "GPHouse"),
    ("Khulna Circle Office", "Khulna Circle Office"),
    ("Chattaogram Regional Office", "Chattogram Regional Office"),
    ("Cumilla Regional Office", "Cumilla Regional Office"),
    ("Chattogram Circle Office", "Chattogram Circle Office"),
    ("Bogra Regional Office", "Bogra Regional Office"),
    ("Dinajpur Area Office", "Dinajpur Area Office"),
    ("GP House", "GP House"),
    ("Mothijheel Area Office", "Mothijheel Area Office"),
    ("Gazipur Regional Office", "Gazipur Regional Office"),
    ("Sylhet Circle Office", "Sylhet Circle Office"),
    ("Jessore Area Office", "Jessore Area Office"),
    ("Savar Area Office", "Savar Area Office"),
    ("Dhanmondi Area Office", "Dhanmondi Area Office"),
    ("Rajshahi Circle Office", "Rajshahi Circle Office"),
    ("Barisal Regional Office", "Barisal Regional Office"),
    ("Habiganj Area Office", "Habiganj Area Office"),
    ("Comilla Regional Office", "Comilla Regional Office"),
    ("Mymensingh Regional Office", "Mymensingh Regional Office"),
    ("Tangail Area Office", "Tangail Area Office"),
    ("Pabna Area Office", "Pabna Area Office"),
    ("Faridpur Area Office", "Faridpur Area Office"),
    ("Karwan Rre Nzzice", "Karwan Rre Nzzice"),
    ("Norshindi Area Office", "Norshindi Area Office"),
    ("Noakhali Area Office", "Noakhali Area Office"),
    ("Narayanganj Area Office", "Narayanganj Area Office"),
]

class GPUser(models.Model):

    SUPERADMIN = "Superadmin"
    KAM = "KAM"
    COPC = "COPC"
    VA = "VA"
    LERP = "LERP"
    GERP = "GERP"
    DA = "DA"
    CLC = "CLC"
    MANAGER = "Manager"
    SEGMENT_LEADER = "Leader"

    SME = "SME"
    LCA = "LCA"

    SEGMENTS = [
        (SME, "SME"),
        (LCA, "LCA"),
    ]

    ROLES = [
        (SUPERADMIN, "Super Admin"),
        (KAM, "KAM"),
        (COPC, "COPC"),
        (VA, "VA"),
        (LERP, "LERP"),
        (GERP, "GERP"),
        (CLC, "CLC"),
        (DA, "DA"),
        (MANAGER, "Manager"),
        (SEGMENT_LEADER, "Leader"),
    ]

    phone_number = models.CharField(max_length=255, primary_key=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True)
    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default=KAM,
    )
    
    segment = models.CharField(
        max_length=10,
        choices=SEGMENTS,
        default=SME,
    )

    pass_change_code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )

class KAMTable(models.Model):
    emp_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    employee_name = models.CharField(
        max_length=255,
        primary_key=True,
        blank=True
    )

    department = models.CharField(
        max_length=255,
        choices=SUBSEGMENTS,
        blank=True,
        null=True,
    )

    mobile_number = models.CharField(
        max_length=11,
        null=True,
        blank=True,
    )

    location = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    username = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    manager = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

class Ticket(models.Model):

    WORKFLOW_TYPES = [
        (OBDG, "Onboarding"),
    ]

    corporate_name = models.CharField(
        max_length=255,
    )

    
    WFID = models.CharField(
        max_length=255,
        primary_key=True,
    )

    bs_code = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    global_status = models.CharField(
        max_length=255,
        choices=STATUSES,
        null=True,
        blank=True
    )

    first_issued_datetime = models.DateTimeField(
        null=True,
        blank=True
    )
    last_update_datetime = models.DateTimeField(
        null=True,
        blank=True
    )
    
    WFType = models.CharField(
        max_length=100,
        choices=WORKFLOW_TYPES,
    )

    current_stage = models.CharField(
        max_length=255,
    )

    completed_stages = models.TextField(
        blank=True,
        null=True
    )

    pending_to = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    remarks = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    kam_owner = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    
class Onboarding(models.Model):

    # THESE ARE THE SUBSEGMENTS #
    PRIME = "Prime Account"
    SLA = "Strategic and Large Account"
    EA = "Emerging Accounts"
    GA = "Government Accounts"
    
    SUBSEGMENTS = [
        (PRIME, "Prime Account"),
        (SLA, "Strategic and Large Account"),
        (EA, "Emerging Accounts"),
        (GA, "Government Accounts"),
    ]
    # SUBSEGMENT ENDS #


    # ZONE START #

    Z1 =  "Emerging Accounts 1"
    Z2 =  "Government Accounts"
    Z3 =  "Large Account 1"
    Z4 =  "Large Account 2"
    Z5 =  "Large Account 3"
    Z6 =  "Large Account 4"
    Z7 =  "Prime Accounts 1"
    Z8 =  "Prime Accounts 2"
    Z9 =  "Prime Accounts 3"
    Z10 =  "Prime Accounts 4"
    Z11 =  "Prime Accounts Chattogram"
    Z12 =  "SME Circle Chattogram"
    Z13 =  "SME Circle Dhaka"
    Z14 =  "SME Circle Gazipur"
    Z15 =  "SME Circle Khulna"
    Z16 =  "SME Circle Rajshahi"
    Z17 =  "SME Circle Sylhet"
    Z18 =  "Strategic Accounts 1"
    Z19 =  "Strategic Accounts 2"
    Z20 =  "Strategic Accounts 3"

    ZONES = [
        (Z1, "Emerging Accounts 1"),
        (Z2, "Government Accounts"),
        (Z3, "Large Account 1"),
        (Z4, "Large Account 2"),
        (Z5, "Large Account 3"),
        (Z6, "Large Account 4"),
        (Z7, "Prime Accounts 1"),
        (Z8, "Prime Accounts 2"),
        (Z9, "Prime Accounts 3"),
        (Z10, "Prime Accounts 4"),
        (Z11, "Prime Accounts Chattogram"),
        (Z12, "SME Circle Chattogram"),
        (Z13, "SME Circle Dhaka"),
        (Z14, "SME Circle Gazipur"),
        (Z15, "SME Circle Khulna"),
        (Z16, "SME Circle Rajshahi"),
        (Z17, "SME Circle Sylhet"),
        (Z18, "Strategic Accounts 1"),
        (Z19, "Strategic Accounts 2"),
        (Z20, "Strategic Accounts 3"),
    ]

    # ZONE END #
    

    # CORPORATE TYPES #

    COCP = "COCP"
    COIP = "COIP"

    CORPORATE_TYPES = [
        (COCP, "COCP"),
        (COIP, "COIP"),
    ]

    # CORPORATE TYPES END #


    # REGIONS #

    R1 = "Region 1"
    R2 = "Region 2"
    R3 = "Region 3"

    REGIONS = [
        (R1, "Region 1"),
        (R2, "Region 2"),
        (R3, "Region 3"),
    ]

    # REGIONS END #

    # SEGMENTS START #
    SME = "SME"
    LCA = "LCA"

    SEGMENTS = [
        (SME, "SME"),
        (LCA, "LCA"),
    ]

    # SEGMENTS END #

    # DISTRICTS START #

    D1 = "District 1"
    D2 = "District 2"

    DISTRICTS = [
        (D1, "District 1"),
        (D2, "District 2"),
    ]

    # DISTRICTS END #

    # THANAS START #

    RP1 = "Rate Plan 1"
    RP2 = "Rate Plan 2"

    RATEPLANS = [
        (RP1, "Rate Plan 1"),
        (RP2, "Rate Plan 2"),
    ]

    # THANAS END #


    # THANAS START #

    T1 = "Thanas 1"
    T2 = "Thanas 2"

    THANAS = [
        (T1, "Thanas 1"),
        (T2, "Thanas 2"),
    ]

    # THANAS END #

    # CUG ID START #

    CUG1 = "CUG 1"
    CUG2 = "CUG 2"

    CUGID = [
        (CUG1, "CUG 1"),
        (CUG2, "CUG 2"),
    ]

    PULSES = [
        ("1 Second", "1 Second"),
        ("10 Second", "10 Second")
    ]

    CUG_PULSES = [
        ("1 Second", "1 Second"),
        ("10 Second", "10 Second")
    ]

    # THANAS END #

    corporate_name = models.CharField(
        max_length=255,
        primary_key=True,
    )

    corporate_short_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    bscode = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    subsegment = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        choices=SUBSEGMENTS
    )

    zone = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        choices=ZONES
    )
    
    parent_bscode = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    corporate_type = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        choices=CORPORATE_TYPES,
    )

    kam_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    kam_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )


    bs_customer_region = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=REGIONS
    )

    address1 = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    address2 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    district = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=DISTRICTS
    )

    thana = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=THANAS
    )

    zip_code = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    city = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    gerp_address = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    rate = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=RATEPLANS,
    )

    cug_id = models.CharField(
        max_length=255,
        choices=CUGID,
        blank=True,
        null=True,
    )

    pulse = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    cug_pulse = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    vid = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    bill_cycle = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    vat_waiver_flag = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    wo_ca_attach = models.CharField(max_length=255, null=True, blank=True)
    btrc_form_1000 = models.CharField(max_length=255, null=True, blank=True)
    proof_of_company_id = models.CharField(max_length=255, null=True, blank=True)
    btrc_form = models.CharField(max_length=255, null=True, blank=True)
    btrc_form_2 = models.CharField(max_length=255, null=True, blank=True)
    btrc_form_3 = models.CharField(max_length=255, null=True, blank=True)
    nid_authorized = models.CharField(max_length=255, null=True, blank=True)
    proof_of_company_billing_address = models.CharField(max_length=255, null=True, blank=True)
    agreement_copy = models.CharField(max_length=255, null=True, blank=True)
    approved_ams = models.CharField(max_length=255, null=True, blank=True)

    kcp_first_name = models.CharField(max_length=255, null=True, blank=True)
    kcp_last_name = models.CharField(max_length=255, null=True, blank=True)
    kcp_contact_number = models.CharField(max_length=255, null=True, blank=True)
    kcp_email_1 = models.CharField(max_length=255, null=True, blank=True)
    kcp_email_2 = models.CharField(max_length=255, null=True, blank=True)
    kcp_email_3 = models.CharField(max_length=255, null=True, blank=True)
    kcp_nid = models.CharField(max_length=255, null=True, blank=True)

    kcp_dob = models.DateField(
        blank=True,
        null=True
    )

    erp_company_code = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    onboarded = models.BooleanField(
        blank=True,
        null=True,
    )

    btrc_approved_govt_organization = models.BooleanField(
        blank=True,
        null=True,
    )

class Item(models.Model):
    item_code = models.CharField(
        max_length=255,
        primary_key=True,
    )

    description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    ITEM_TYPES = [
        ("PHYSICAL CONN", "PHYSICAL CONN"),
        ("DEVICE", "DEVICE"),
        ("VIRTUAL CONN", "VIRTUAL CONN"),
    ]

    item_type = models.CharField(
        max_length=255,
        choices=ITEM_TYPES,
        blank=True
    )


class ProductRequisition(models.Model):
    wfid = models.CharField(max_length=255, primary_key=True)
    kam_id = models.CharField(max_length=255, null=True, blank=True)
    kam_name = models.CharField(max_length=255, null=True, blank=True)
    kam_mobile = models.CharField(max_length=255, null=True, blank=True)
    kam_designation = models.CharField(max_length=255, null=True, blank=True)
    kam_email = models.CharField(max_length=255, null=True, blank=True)
    kam_location = models.CharField(max_length=255, null=True, blank=True)
    kam_department = models.CharField(max_length=255, null=True, blank=True)
    bs_code = models.CharField(max_length=255, null=True, blank=True)
    corporate_name = models.CharField(max_length=255, null=True, blank=True)
    sub_segment = models.CharField(max_length=255, null=True, blank=True)
    zone = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    erp_code = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.CharField(max_length=255, null=True, blank=True)
    unit_price = models.CharField(max_length=255, null=True, blank=True)
    total_price = models.CharField(max_length=255, null=True, blank=True)


    client_contact_person = models.CharField(max_length=255, null=True, blank=True)
    client_mobile_number = models.CharField(max_length=255, null=True, blank=True)
    product_delivery_address = models.CharField(max_length=255, null=True, blank=True)
    
    authorized_person_name = models.CharField(max_length=255, null=True, blank=True)
    authorized_person_contact_no = models.CharField(max_length=255, null=True, blank=True)
    authorized_person_email = models.CharField(max_length=255, null=True, blank=True)
    authorized_person_designation = models.CharField(max_length=255, null=True, blank=True)
    authorized_person_nid_number = models.CharField(max_length=255, null=True, blank=True)
    
    remarks = models.CharField(max_length=255, null=True, blank=True)
    
    total_employee = models.CharField(max_length=255, null=True, blank=True)
    total_sim = models.CharField(max_length=255, null=True, blank=True)
    bsm_authorized_person_name = models.CharField(max_length=255, null=True, blank=True)
    bsm_authorized_person_nid_number = models.CharField(max_length=255, null=True, blank=True)
    applicable_district = models.CharField(max_length=255, null=True, blank=True)
    
    
    
    
    bde_name = models.CharField(max_length=255, null=True, blank=True)
    bde_pos_code = models.CharField(max_length=255, null=True, blank=True)
    btrc_approval_type = models.CharField(max_length=255, null=True, blank=True)
    sales_credit_option = models.CharField(max_length=255, null=True, blank=True)
    btrc_approval_option = models.CharField(max_length=255, null=True, blank=True)
    btrc_approval_taken_option = models.CharField(max_length=255, null=True, blank=True)



    work_order_application = models.CharField(max_length=255, null=True, blank=True)
    btrc_form_20191000 = models.CharField(max_length=255, null=True, blank=True)
    poc_id = models.CharField(max_length=255, null=True, blank=True)
    btrc_form_20191001 = models.CharField(max_length=255, null=True, blank=True)
    btrc_form_20191002 = models.CharField(max_length=255, null=True, blank=True)
    nid_kcp = models.CharField(max_length=255, null=True, blank=True)
    poc_billing_address = models.CharField(max_length=255, null=True, blank=True)
    agreement_copy = models.CharField(max_length=255, null=True, blank=True)
    ams_start_up = models.CharField(max_length=255, null=True, blank=True)
    ams_rate_plan = models.CharField(max_length=255, null=True, blank=True)
    ams_both = models.CharField(max_length=255, null=True, blank=True)
    other = models.CharField(max_length=255, null=True, blank=True)
    previous_btrc_form_20191000 = models.CharField(max_length=255, null=True, blank=True)
    previous_btrc_form_20191003 = models.CharField(max_length=255, null=True, blank=True)

    deal_closed = models.BooleanField(
        null=True,
        blank=True,
    )


class TaskVsWFID(models.Model):
    wfid = models.CharField(max_length=255, null=False, blank=False, primary_key=True);
    task_identifier = models.CharField(max_length=255, null=False, blank=False)
    workflow_type =models.CharField(
        max_length=255,
        choices=WORKFLOW_TYPES,
    )


class SLA(models.Model):
    '''
        WFID: The workflow ID of the SLA.
        Task: The task/stage of the SLA.
        User Identifier: The user_identifier of the SLA. That is, who is the person.
        Together these three things make up the searchable primary key.
        Status: Indicates whether the task is complete or not.
    '''

    wfid = models.CharField(max_length=255, null=False, blank=False)
    task = models.CharField(max_length=255, null=False, blank=False)

    workflow_type = models.CharField(max_length=255, null=False, blank=False)
    fire_time = models.DateTimeField(
        null=True,
        blank=True
    )
    completion_time = models.DateTimeField(
        null=True,
        blank=True
    )
    expected_difference = models.FloatField(
        null=True,
        blank=True,
    )
    actual_difference = models.FloatField(
        null=True,
        blank=True
    )
    user_identifier = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    status = models.BooleanField(
        null=True,
        blank=True
    )


# Roles are now created by the super admin, and dynamic.
class Role(models.Model):
    role = models.CharField(
        max_length=255,
        primary_key=True,
    )

# Tasks are now created by the super admin, and dynamic.
class Task(models.Model):
    task = models.CharField(
        max_length=255,
        primary_key=True,
    )

class TaskVsSLA(models.Model):
    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE, 
        primary_key=True,   
    )
    SLA = models.FloatField()

# Each Task now has a list of roles associated with it. Seperator is ';'
class TaskVsRole(models.Model):
    # IMPORTANT: Separator is ';'.

    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE, 
        primary_key=True,   
    )

    permitted = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )
