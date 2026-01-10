/* ============================================
   Name Input Handler (About Page)
   ============================================ */
function handleNameInput(value) {
  const teamMembersContainer = document.getElementById('team-members');
  const clearBtn = document.getElementById('clear-name-btn');

  // Remove existing dynamic member (if any)
  const existingDynamic = document.getElementById('dynamic-team-member');
  if (existingDynamic) {
    existingDynamic.remove();
  }

  if (value.trim()) {
    // Show clear button
    clearBtn.style.display = 'block';

    // Create new team member
    const memberDiv = document.createElement('div');
    memberDiv.className = 'team-member';
    memberDiv.id = 'dynamic-team-member';
    memberDiv.innerHTML = `
      <div class="team-avatar">${value.charAt(0).toUpperCase()}</div>
      <div class="team-info">
        <h4>${value}</h4>
        <p class="team-role">Team Member</p>
        <p class="team-bio">Welcome to our team! Your contribution helps make skincare safer for everyone.</p>
      </div>
    `;
    teamMembersContainer.appendChild(memberDiv);
  } else {
    // Hide clear button
    clearBtn.style.display = 'none';
  }
}

function clearName() {
  document.getElementById('name-input').value = '';
  handleNameInput('');
}
