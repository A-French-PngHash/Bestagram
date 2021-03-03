//
//  resizeImageExtension.swift
//  Bestagram
//
//  Created by Titouan Blossier on 03/03/2021.
//

import UIKit

extension UIImage {
    /// Resize image by keeping only the center part and removing the bands at the sides (top-bottom/left-right)
    ///
    /// - parameter sideLength: Side of the resized image.
    /// - parameter async: Wether or not to perform this operation asynchronously.
    /// - parameter finishedResizing: Closure called when the resizing is finished. Note that this is only called if the async parameter is set to true.
    ///
    /// - returns: If the operation is not marked as async then this methods returns the new image.
    func makeResizedImage(sideLength : CGFloat, async : Bool = false, finishedResizing : ((UIImage) -> Void)? = nil) -> UIImage? {

        if async {
            DispatchQueue.main.async {
                let newImage = self.af.imageAspectScaled(toFill: CGSize(width: sideLength, height: sideLength))
                if let closure = finishedResizing {
                    closure(newImage)
                } else {
                    fatalError("The function was set as async but no closure was provided.")
                }
            }
        } else {
            let newImage = self.af.imageAspectScaled(toFill: CGSize(width: sideLength, height: sideLength))
            return newImage
        }
        // async operation
        return nil
    }
}
