export default function OverdueLoansModal({ loans, bookTitles, onClose }) {
  if (!loans || loans.length === 0) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
      <div className="bg-white rounded-lg shadow-lg max-w-md w-full p-6">
        <div className="flex items-start gap-3">
          <span className="text-2xl">⚠️</span>
          <div>
            <h2 className="text-lg font-bold text-gray-900">
              You have overdue books
            </h2>
            <p className="text-sm text-gray-600 mt-1">
              The return deadline has passed for the{' '}
              {loans.length === 1 ? 'book below' : 'books below'}. Please return{' '}
              {loans.length === 1 ? 'it' : 'them'} as soon as you can.
            </p>
          </div>
        </div>

        <ul className="mt-4 space-y-2 max-h-48 overflow-y-auto">
          {loans.map((loan) => (
            <li
              key={loan.id}
              className="text-sm bg-red-50 text-red-700 rounded-md px-3 py-2 flex justify-between"
            >
              <span>{bookTitles[loan.book_id] ?? loan.book_id}</span>
              <span className="text-red-500">
                Due:{' '}
                {new Date(loan.due_date).toLocaleDateString('en-GB', {
                  day: '2-digit',
                  month: '2-digit',
                  year: 'numeric',
                })}
              </span>
            </li>
          ))}
        </ul>

        <button
          onClick={onClose}
          className="mt-5 w-full bg-brand-600 hover:bg-brand-700 text-white text-sm py-2 rounded-md transition"
        >
          Got it
        </button>
      </div>
    </div>
  )
}
