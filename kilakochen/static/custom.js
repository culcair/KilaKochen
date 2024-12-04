const ID_RE = /(-)_(-)/;

/**
 * Replace the template index of an element (-_-) with the
 * given index.
 */
function replaceTemplateIndex(value, index) {
    return value.replace(ID_RE, '$1' + index + '$2');
}

/**
 * Adjust the indices of form fields when removing items.
 */
function adjustIndices(removedIndex) {
    const forms = document.querySelectorAll('.subform');

    forms.forEach(function(form, i) {
        let index = parseInt(form.dataset.index);
        let newIndex = index - 1;

        if (index < removedIndex) {
            // Skip
            return;
        }

        // This will replace the original index with the new one
        // only if it is found in the format -num-, preventing
        // accidental replacing of fields that may have numbers
        // in their names.
        let regex = new RegExp('(-)' + index + '(-)');
        let repVal = '$1' + newIndex + '$2';

        // Change ID in form itself
        form.id = form.id.replace(index, newIndex);
        form.dataset.index = newIndex;

        // Change IDs in form fields
        const fields = form.querySelectorAll('label, input, select, textarea');

        fields.forEach(function(item) {
            if (item.tagName.toLowerCase() === 'label') {
                // Update labels
                item.htmlFor = item.htmlFor.replace(regex, repVal);
            } else {
                // Update other fields
                item.id = item.id.replace(regex, repVal);
                item.name = item.name.replace(regex, repVal);
            }
        });
    });
}

/**
 * Remove a form.
 */
function removeForm() {
    const removedForm = this.closest('.subform');
    const removedIndex = parseInt(removedForm.dataset.index);

    removedForm.remove();

    // Update indices
    adjustIndices(removedIndex);
}

/**
 * Add a new form.
 */
function addForm() {
    const templateForm = document.querySelector('#ingredients-_-form');

    if (!templateForm) {
        console.log('[ERROR] Cannot find template');
        return;
    }

    // Get Last index
    const lastForm = document.querySelector('.subform:last-of-type');
    let newIndex = 0;

    if (lastForm) {
        newIndex = parseInt(lastForm.dataset.index) + 1;
    }

    // Maximum of 20 subforms
    if (newIndex >= 20) {
        console.log('[WARNING] Reached maximum number of elements (20)');
        return;
    }

    // Clone the template form
    const newForm = templateForm.cloneNode(true);

    // Update attributes and data
    newForm.id = replaceTemplateIndex(newForm.id, newIndex);
    newForm.dataset.index = newIndex;

    const fields = newForm.querySelectorAll('label, input, select, textarea');

    fields.forEach(function(item) {
        if (item.tagName.toLowerCase() === 'label') {
            // Update labels
            item.htmlFor = replaceTemplateIndex(item.htmlFor, newIndex);
        } else {
            // Update other fields
            item.id = replaceTemplateIndex(item.id, newIndex);
            item.name = replaceTemplateIndex(item.name, newIndex);
        }
    });

    // Append to the list
    document.querySelector('#ingredients-list').appendChild(newForm);
    newForm.classList.add('subform');
    newForm.classList.remove('d-none');

    // Attach remove event listener to the new form
    newForm.querySelector('.remove').addEventListener('click', removeForm);
}

// When the DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    const addButtons = document.querySelectorAll('.add.btn');
    const removeButtons = document.querySelectorAll('.remove.btn');

    addButtons.forEach(function(button) {
        button.addEventListener('click', addForm);
    });

    removeButtons.forEach(function(button) {
        button.addEventListener('click', removeForm);
    });
});
