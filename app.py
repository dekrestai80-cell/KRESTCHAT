// LOGIN - 
async function login() {
  let user = await supabase.from('profiles')
    .select('*')
    .eq('username', username)
    .eq('password', password)
    .single();
  
  if(user) {
    // ENTER - show followers, likes, viewers
    window.location = "/profile.html?user=" + user.username;
  } else {
    alert("Wrong username/password - try SIGN UP");
  }
}

// SIGN UP - for new users only
async function signup() {
  let { error } = await supabase.from('profiles').insert({
    username: username,
    phone: phone,
    followers_count: 0,
    following_count: 0,
    likes_count: 0,
    is_live: false
  });
  
  if(!error) window.location = "/profile.html";
}
