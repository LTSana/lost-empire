// JavaScript for Account Security

document.querySelector("#opwd_visible_toggle").onclick = () => {
	if (document.querySelector("#opwd").type === "password") {
		document.querySelector("#opwd").type = "text"
		document.querySelector("#opwd_visible_toggle").classList.toggle("fa-eye", true)
		document.querySelector("#opwd_visible_toggle").classList.toggle("fa-eye-slash", false)
	} else {
		document.querySelector("#opwd").type = "password"
		document.querySelector("#opwd_visible_toggle").classList.toggle("fa-eye", false)
		document.querySelector("#opwd_visible_toggle").classList.toggle("fa-eye-slash", true)
	}
}

document.querySelector("#npwd_visible_toggle").onclick = () => {
	if (document.querySelector("#npwd").type === "password") {
		document.querySelector("#npwd").type = "text"
		document.querySelector("#npwd_visible_toggle").classList.toggle("fa-eye", true)
		document.querySelector("#npwd_visible_toggle").classList.toggle("fa-eye-slash", false)
	} else {
		document.querySelector("#npwd").type = "password"
		document.querySelector("#npwd_visible_toggle").classList.toggle("fa-eye", false)
		document.querySelector("#npwd_visible_toggle").classList.toggle("fa-eye-slash", true)
	}
}

document.querySelector("#cpwd_visible_toggle").onclick = () => {
	if (document.querySelector("#cpwd").type === "password") {
		document.querySelector("#cpwd").type = "text"
		document.querySelector("#cpwd_visible_toggle").classList.toggle("fa-eye", true)
		document.querySelector("#cpwd_visible_toggle").classList.toggle("fa-eye-slash", false)
	} else {
		document.querySelector("#cpwd").type = "password"
		document.querySelector("#cpwd_visible_toggle").classList.toggle("fa-eye", false)
		document.querySelector("#cpwd_visible_toggle").classList.toggle("fa-eye-slash", true)
	}
}
