(function() {
    'use strict';
    
    window.addEventListener('load', function() {
        var divisionSelect = document.getElementById('id_division');
        var deptSelect = document.getElementById('id_dept');
        var sectionSelect = document.getElementById('id_section');
        
        function filterDept() {
            var divisionId = divisionSelect.value;
            if (divisionId) {
                fetch('/hr/api/dept-by-division/?division_id=' + divisionId)
                    .then(response => response.json())
                    .then(data => {
                        deptSelect.innerHTML = '<option value="">---------</option>';
                        data.forEach(function(dept) {
                            var option = document.createElement('option');
                            option.value = dept.id;
                            option.textContent = dept.nama;
                            deptSelect.appendChild(option);
                        });
                        filterSection(); // reset section
                    });
            } else {
                deptSelect.innerHTML = '<option value="">---------</option>';
                sectionSelect.innerHTML = '<option value="">---------</option>';
            }
        }
        
        function filterSection() {
            var deptId = deptSelect.value;
            if (deptId) {
                fetch('/hr/api/section-by-dept/?dept_id=' + deptId)
                    .then(response => response.json())
                    .then(data => {
                        sectionSelect.innerHTML = '<option value="">---------</option>';
                        data.forEach(function(section) {
                            var option = document.createElement('option');
                            option.value = section.id;
                            option.textContent = section.nama;
                            sectionSelect.appendChild(option);
                        });
                    });
            } else {
                sectionSelect.innerHTML = '<option value="">---------</option>';
            }
        }
        
        divisionSelect.addEventListener('change', filterDept);
        deptSelect.addEventListener('change', filterSection);
        filterDept();
    });
})();