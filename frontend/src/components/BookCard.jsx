import { useState } from 'react'

const MAX_LOAN_DAYS = 20
const DEFAULT_LOAN_DAYS = 14

export default function BookCard({ book, onBorrow, isAdmin, onEdit, onDelete, myActiveCount = 0 }) {
  const isAvailable = book.available_copies > 0
  const [durationDays, setDurationDays] = useState(DEFAULT_LOAN_DAYS)
  const [quantity, setQuantity] = useState(1)

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 flex flex-col justify-between">
      <div>
        <h3 className="font-semibold text-gray-900">{book.title}</h3>
        <p className="text-sm text-gray-500">{book.author}</p>
        {book.category && (
          <span className="inline-block mt-2 text-xs bg-brand-50 text-brand-700 px-2 py-0.5 rounded-full">
            {book.category}
          </span>
        )}
        <p className="text-sm mt-2 text-gray-600">
          Available: <span className="font-medium">{book.available_copies}</span> / {book.total_copies}
        </p>
        {myActiveCount > 0 && (
          <p className="text-xs mt-1 text-amber-600">
            You are currently renting {myActiveCount} {myActiveCount === 1 ? 'copy' : 'copies'}
          </p>
        )}
      </div>

      {!isAdmin && onBorrow && isAvailable && (
        <div className="mt-3 space-y-2">
          <div>
            <label className="block text-xs text-gray-500 mb-1">
              Copies to borrow (up to {book.available_copies} available)
            </label>
            <input
              type="number"
              min={1}
              max={book.available_copies}
              value={Math.min(quantity, book.available_copies)}
              onChange={(e) => {
                const value = Number(e.target.value)
                if (Number.isNaN(value)) return
                setQuantity(Math.min(book.available_copies, Math.max(1, value)))
              }}
              className="w-full border border-gray-300 rounded-md px-2 py-1 text-sm"
            />
          </div>
          <div>
            <label className="block text-xs text-gray-500 mb-1">
              Return deadline (days, up to {MAX_LOAN_DAYS})
            </label>
            <input
              type="number"
              min={1}
              max={MAX_LOAN_DAYS}
              value={durationDays}
              onChange={(e) => {
                const value = Number(e.target.value)
                if (Number.isNaN(value)) return
                setDurationDays(Math.min(MAX_LOAN_DAYS, Math.max(1, value)))
              }}
              className="w-full border border-gray-300 rounded-md px-2 py-1 text-sm"
            />
          </div>
        </div>
      )}

      <div className="mt-4 flex gap-2">
        {!isAdmin && onBorrow && (
          <button
            onClick={() => onBorrow(book.id, durationDays, Math.min(quantity, book.available_copies))}
            disabled={!isAvailable}
            className="flex-1 bg-brand-600 hover:bg-brand-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white text-sm py-1.5 rounded-md transition"
          >
            {isAvailable ? 'Borrow' : 'Not available'}
          </button>
        )}
        {isAdmin && (
          <>
            <button
              onClick={() => onEdit(book)}
              className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm py-1.5 rounded-md transition"
            >
              Edit
            </button>
            <button
              onClick={() => onDelete(book.id)}
              className="flex-1 bg-red-50 hover:bg-red-100 text-red-600 text-sm py-1.5 rounded-md transition"
            >
              Delete
            </button>
          </>
        )}
      </div>
    </div>
  )
}
