document.addEventListener('DOMContentLoaded', () => {
  const input = document.querySelector('input[type="file"][name="image"]')
  const img = document.getElementById('imgPreview')
  if (!input || !img) return

  input.addEventListener('change', () => {
    const [file] = input.files
    if (file) {
      img.src = URL.createObjectURL(file)
    }
  })
})
