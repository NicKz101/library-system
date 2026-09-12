const statusStyles = {
  ACTIVE: 'bg-blue-50 text-blue-700',
  OVERDUE: 'bg-red-50 text-red-700',
  RETURNED: 'bg-green-50 text-green-700',
}

function formatDateTime(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export default function LoanTable({ loans, onReturn, showMemberColumn, bookTitles = {}, memberNames = {} }) {
  if (loans.length === 0) {
    return <p className="text-gray-500 text-sm">No loans to show.</p>
  }

  return (
    <div className="overflow-x-auto bg-white rounded-lg border border-gray-200">
      <table className="min-w-full text-sm">
        <thead className="bg-gray-50 text-gray-600 text-left">
          <tr>
            <th className="px-4 py-2">Book</th>
            {showMemberColumn && <th className="px-4 py-2">Member</th>}
            <th className="px-4 py-2">Borrowed on</th>
            <th className="px-4 py-2">Due date</th>
            <th className="px-4 py-2">Returned on</th>
            <th className="px-4 py-2">Status</th>
            {onReturn && <th className="px-4 py-2"></th>}
          </tr>
        </thead>
        <tbody>
          {loans.map((loan) => (
            <tr
              key={loan.id}
              className={`border-t border-gray-100 ${
                loan.status === 'OVERDUE' ? 'bg-red-50/60' : ''
              }`}
            >
              <td className="px-4 py-2">{bookTitles[loan.book_id] ?? loan.book_id}</td>
              {showMemberColumn && (
                <td className="px-4 py-2">{memberNames[loan.member_id] ?? loan.member_id}</td>
              )}
              <td className="px-4 py-2 whitespace-nowrap">{formatDateTime(loan.loan_date)}</td>
              <td className="px-4 py-2 whitespace-nowrap">{formatDateTime(loan.due_date)}</td>
              <td className="px-4 py-2 whitespace-nowrap">{formatDateTime(loan.return_date)}</td>
              <td className="px-4 py-2">
                <span className={`px-2 py-0.5 rounded-full text-xs ${statusStyles[loan.status]}`}>
                  {loan.status}
                </span>
              </td>
              {onReturn && (
                <td className="px-4 py-2">
                  {loan.status !== 'RETURNED' && (
                    <button
                      onClick={() => onReturn(loan.id)}
                      className="text-brand-600 hover:underline text-xs"
                    >
                      Return
                    </button>
                  )}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
