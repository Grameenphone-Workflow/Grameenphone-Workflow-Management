function generateTicketTable(id) {
    $(id).DataTable({
        "ajax": "../fetch_tickets/",
        "columns": [
            { "data": "WFID" },
            { "data": "Workflow Type" },
            { "data": "BS Code" },
            { "data": "Global Status" },
            { "data": "First Issued" },
            { "data": "Last Updated" },
            { "data": "Current Stage" },
            { "data": "Pending To" }
        ],
        dom: 'Bfrtip',
        "buttons": [
            'copy', 'csv', 'excel',
        ],
        pageLength: 10,
        filter: true,
        scrollCollapse: true,
        scroller: true,
        responsive: true
    });
}