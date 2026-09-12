import { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { listBooks, createBook, updateBook, deleteBook } from '../api/books'
import { borrowBook, myLoans } from '../api/loans'
import BookCard from '../components/BookCard'

const emptyForm = { title: '', author: '', isbn: '', category: '', total_copies: 1 }

export default function BooksPage() {
  const { isAdmin } = useAuth()
  const [books, setBooks] = useState([])
  const [myActiveCounts, setMyActiveCounts] = useState({})
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [form, setForm] = useState(emptyForm)

  async function loadBooks() {
    setLoading(true)
    try {
      // Admins don't borrow books, so there's no point asking for their loans.
      const [booksData, loansData] = await Promise.all([
        listBooks(),
        isAdmin ? Promise.resolve([]) : myLoans(),
      ])
      setBooks(booksData)

      const counts = {}
      for (const loan of loansData) {
        if (loan.status !== 'RETURNED') {
          counts[loan.book_id] = (counts[loan.book_id] ?? 0) + 1
        }
      }
      setMyActiveCounts(counts)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadBooks()
  }, [])

  async function handleBorrow(bookId, durationDays, quantity) {
    setMessage(null)
    try {
      await borrowBook(bookId, durationDays, quantity)
      setMessage({
        type: 'success',
        text: `${quantity} cop${quantity === 1 ? 'y' : 'ies'} borrowed successfully!`,
      })
      loadBooks()
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail ?? 'Could not borrow this book' })
    }
  }

  function openCreateForm() {
    setForm(emptyForm)
    setEditingId(null)
    setShowForm(true)
  }

  function openEditForm(book) {
    setForm({
      title: book.title,
      author: book.author,
      isbn: book.isbn,
      category: book.category ?? '',
      total_copies: book.total_copies,
    })
    setEditingId(book.id)
    setShowForm(true)
  }

  async function handleSubmitForm(e) {
    e.preventDefault()
    setMessage(null)
    try {
      if (editingId) {
        const { isbn, ...updatable } = form // ISBN is not editable
        await updateBook(editingId, { ...updatable, total_copies: Number(form.total_copies) })
      } else {
        await createBook({ ...form, total_copies: Number(form.total_copies) })
      }
      setShowForm(false)
      loadBooks()
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail ?? 'Could not save the book' })
    }
  }

  async function handleDelete(bookId) {
    if (!confirm('Are you sure you want to delete this book?')) return
    try {
      await deleteBook(bookId)
      loadBooks()
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail ?? 'Could not delete the book' })
    }
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Book Catalog</h1>
        {isAdmin && (
          <button
            onClick={openCreateForm}
            className="bg-brand-600 hover:bg-brand-700 text-white text-sm px-4 py-2 rounded-md transition"
          >
            + New book
          </button>
        )}
      </div>

      {message && (
        <div
          className={`mb-4 text-sm px-4 py-2 rounded-md ${
            message.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
          }`}
        >
          {message.text}
        </div>
      )}

      {showForm && (
        <form
          onSubmit={handleSubmitForm}
          className="mb-6 bg-white border border-gray-200 rounded-lg p-4 grid grid-cols-2 gap-3"
        >
          <input
            placeholder="Title"
            required
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            className="border border-gray-300 rounded-md px-3 py-2 text-sm"
          />
          <input
            placeholder="Author"
            required
            value={form.author}
            onChange={(e) => setForm({ ...form, author: e.target.value })}
            className="border border-gray-300 rounded-md px-3 py-2 text-sm"
          />
          <input
            placeholder="ISBN"
            required
            disabled={!!editingId}
            value={form.isbn}
            onChange={(e) => setForm({ ...form, isbn: e.target.value })}
            className="border border-gray-300 rounded-md px-3 py-2 text-sm disabled:bg-gray-100"
          />
          <input
            placeholder="Category"
            value={form.category}
            onChange={(e) => setForm({ ...form, category: e.target.value })}
            className="border border-gray-300 rounded-md px-3 py-2 text-sm"
          />
          <input
            type="number"
            min={1}
            placeholder="Total copies"
            required
            value={form.total_copies}
            onChange={(e) => setForm({ ...form, total_copies: e.target.value })}
            className="border border-gray-300 rounded-md px-3 py-2 text-sm"
          />
          <div className="flex gap-2 col-span-2">
            <button
              type="submit"
              className="bg-brand-600 hover:bg-brand-700 text-white text-sm px-4 py-2 rounded-md transition"
            >
              Save
            </button>
            <button
              type="button"
              onClick={() => setShowForm(false)}
              className="bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm px-4 py-2 rounded-md transition"
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      {loading ? (
        <p className="text-gray-500 text-sm">Loading...</p>
      ) : books.length === 0 ? (
        <p className="text-gray-500 text-sm">There are no books in the catalog yet.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {books.map((book) => (
            <BookCard
              key={book.id}
              book={book}
              isAdmin={isAdmin}
              onBorrow={handleBorrow}
              onEdit={openEditForm}
              onDelete={handleDelete}
              myActiveCount={myActiveCounts[book.id] ?? 0}
            />
          ))}
        </div>
      )}
    </div>
  )
}
