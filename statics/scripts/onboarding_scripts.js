function CheckCorporateNameAvailability(corporateName) {
    if ($('#corporate_name').prop('readonly') == true)
        return;
    if ($('#corporate_name').val() == "")
        return;
    console.log(corporateName);
    $.get("../__get_all_corp_names/",
        {
            corp_name: corporateName,
        },
        function (data, status) {
            if (data == "Exists") {
                $('#corporate_name').val("");
                $('#corporate_name').focus();
                alert("That corporate name already exists");
                return;
            }
            else {
                return false;
            }
        });
}

function CheckBSCodeAvailability(bscode) {
    $.get("../check_bs_code/",
        {
            bscode: bscode,
        },
        function (data, status) {
            if (data == "Exists") {
                $('#bs_code').val("");
                $('#bs_code').focus();
                alert("That BS code already exists");
                return;
            }
            else {
                return false;
            }
        });
}

function ParentChildBSCodeSelection() {
    var bsSelection = document.getElementById('bs_code_type');
    console.log(bsSelection.value);
    if (bsSelection.value == "Parent") {
        console.log($('#bs_code_label').val());
        $('#parent_bs_code').prop('readonly', true);
        $('#bs_code_label').text("BS Code");
    } else if (bsSelection.value == "Child") {
        console.log($('#bs_code_label').val());
        $('#parent_bs_code').prop('readonly', false);
        $('#bs_code_label').text("Child BS Code");
    }

}