async function loadNotes() {
    const response = await fetch('/notes');
    const notes = await response.json();

    const list = document.getElementById('notesList');
    list.innerHTML = '';

    notes.forEach(note => {
        const li = document.createElement('li');
        const textSpan = document.createElement('span');
        textSpan.textContent = note.content;

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.className = 'delete-btn';
        deleteButton.onclick = () => deleteNote(note.id);

        li.appendChild(textSpan);
        li.appendChild(deleteButton);
        list.appendChild(li);
    });
}

async function deleteNote(id) {
    await fetch(`/notes/${id}`, {
        method: 'DELETE'
    });
    loadNotes();
}

async function saveNote() {
    const note = document.getElementById('note').value;

    if (note.trim() === '') return;

    await fetch('/notes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: note })
    });

    document.getElementById('note').value = '';
    loadNotes();
}

loadNotes();