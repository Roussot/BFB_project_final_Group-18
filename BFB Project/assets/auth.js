// assets/auth.js - cleaned ES5-compatible auth helper
// No <script> or markdown wrappers. Exposes AUTH, renderAuthNav, requireRole

var AUTH = (function(){
  var keys = { users:'users', current:'currentUserId' };

  function _loadUsers(){ try { return JSON.parse(localStorage.getItem(keys.users)) || []; } catch (e) { return []; } }
  function _saveUsers(arr){ localStorage.setItem(keys.users, JSON.stringify(arr)); }

  function currentUser(){
    var id = localStorage.getItem(keys.current);
    if(!id) return null;
    var list = _loadUsers();
    for(var i=0;i<list.length;i++){ if(list[i].id === id) return list[i]; }
    return null;
  }

  function currentRole(){
    var u = currentUser();
    return u && u.role ? u.role : null;
  }

  function register(opts){
    opts = opts || {};
    var name = (opts.name || '').trim();
    var email = (opts.email || '').trim().toLowerCase();
    var password = opts.password || '';
    var role = opts.role || '';
    var users = _loadUsers();
    for(var i=0;i<users.length;i++){ if(users[i].email === email) throw new Error('Email already registered.'); }
    var id = (typeof crypto !== 'undefined' && crypto.randomUUID) ? crypto.randomUUID() : Math.random().toString(36).slice(2);
    users.push({ id: id, name: name, email: email, password: password, role: role });
    _saveUsers(users);
    localStorage.setItem(keys.current, id);
    return id;
  }

  function login(email, password){
    email = (email||'').trim().toLowerCase();
    var users = _loadUsers();
    for(var i=0;i<users.length;i++){
      var u = users[i];
      if((u.email||'').trim().toLowerCase() === email && u.password === password){
        localStorage.setItem(keys.current, u.id);
        return u;
      }
    }
    throw new Error('Invalid email or password.');
  }

  function logout(){ localStorage.removeItem(keys.current); }

  return { keys: keys, _loadUsers: _loadUsers, _saveUsers: _saveUsers, currentUser: currentUser, currentRole: currentRole, register: register, login: login, logout: logout };
})();

function renderAuthNav(){
  var u = AUTH.currentUser();
  var role = u && u.role ? u.role : null;

  var loginL      = document.getElementById('navLogin');
  var registerL   = document.getElementById('navRegister');
  var logoutL     = document.getElementById('navLogout');
  var uploadL     = document.getElementById('navUpload');
  var logisticsL  = document.getElementById('navLogistics');
  var marketplaceL= document.getElementById('navMarketplace');
  var userName    = document.getElementById('navUserName');

  if(loginL)    loginL.style.display    = u ? 'none' : '';
  if(registerL) registerL.style.display = u ? 'none' : '';
  if(logoutL)   logoutL.style.display   = u ? '' : 'none';
  if(userName)  userName.textContent    = u ? u.name : '';

  // Keep Upload and Logistics links visible for navigation; pages will enforce role-specific behavior.
  if(uploadL)      uploadL.style.display      = '';
  if(logisticsL)   logisticsL.style.display   = '';

  if(logoutL){
    logoutL.onclick = function(e){ e.preventDefault(); AUTH.logout(); location.href='index.html'; };
  }

  // Make sure login/register links always navigate when clicked (defensive)
  if(loginL){
    loginL.addEventListener('click', function(ev){
      // if the link already points to a page, follow it; else fallback
      var href = loginL.getAttribute('href') || 'login.html';
      location.href = href;
    });
  }
  if(registerL){
    registerL.addEventListener('click', function(ev){
      var href = registerL.getAttribute('href') || 'register.html';
      location.href = href;
    });
  }
}

function requireRole(roles){
  var role = AUTH.currentRole();
  var allowed = Array.isArray(roles) ? roles : [roles];
  if(!role || allowed.indexOf(role) === -1){
    var back = encodeURIComponent(location.pathname + location.search);
    location.href = 'login.html?next=' + back;
  }
}
